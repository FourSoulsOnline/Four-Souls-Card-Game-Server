/* Develper: Oscar Saavedra */

// Bring in express
import express from "express";
// Bring in the cors library
import cors from "cors";
// Create instance of HTTP library
import http from "http";
// Get the Server class from socket.io
import { Server } from "socket.io";
// Get child process library
import childProcess from "child_process";
import zlib from "zlib";

const spawner = childProcess.spawn;

// Use gameServer as an instance of express
const gameServer = express();

// Set the PORT to listen on
const PORT = process.env.PORT || 28018;

// Set the cors options
const corsOptions = {
  origin: "*",
  credentials: true,
};

// Helps prevent connection errors
gameServer.use(cors(corsOptions));

// Create http server with express
const server = http.createServer(gameServer);

// Create variable to use socket.io functions
const io = new Server(server, { cors: corsOptions });

// Get the username from the client and connect it with its socket - O.S.
io.use((socket, next) => {
  const username = socket.handshake.auth.username;
  socket.username = username;
  next();
});

// Function that reformats list of clients in a room - O.S.
function getList(socketsInRoom) {
  let list = [];
  for (const s of socketsInRoom) {
    list.push({ socketID: s.id, username: s.username });
  }
  return list;
}

// Dictionary to store child processes for each room.
const pythonProcesses = {};

// Listen for connection event to know someone connected to server
io.on("connection", async (socket) => {
  // Total clients connected to server
  var totalClients = await io.fetchSockets();

  // Display user information on console when connected
  console.log("TOTAL CLIENTS ON SERVER: " + totalClients.length);
  console.log("User connected: " + socket.id);
  console.log("\tUsername: " + socket.username);

  // Join clients to a specified room - O.S.
  socket.on("join-lobby", async (lobbyCode) => {
    // Set the max number of clients per room - O.S.
    const MAX_CLIENTS = 4;
    // Get the count of clients in room - O.S.
    var socketsInRoom = await io.in(lobbyCode).fetchSockets();

    // Check if the room is full - O.S.
    if (socketsInRoom.length < MAX_CLIENTS) {
      // Add room information to socket - O.S.
      socket.data.room = lobbyCode;
      // Add client to the room - O.S.
      socket.join(lobbyCode);

      // DONT NEED THIS AFTER COMPLETE JUST FOR TESTING_______________
      socketsInRoom = await io.in(lobbyCode).fetchSockets();
      console.log(
        "User: " + socket.username + " connected to lobby (" + lobbyCode + ")"
      );
      console.log("\t Room count: " + socketsInRoom.length);
      //______________________________________________________________

      // List to send back to the client - O.S.
      var users = getList(socketsInRoom);

      // Add to lobby success - O.S.
      socket.emit("join-lobby-success", true);
      // Send list of clients in particular room - O.S.
      io.to(socket.data.room).emit("new-user-response", users);
    } else {
      // Add to lobby failure - O.S.
      socket.emit("join-lobby-success", false);
    }
  });

  // Clients decide to leave room - O.S.
  socket.on("leave-lobby", async (lobbyCode) => {
    // Disconnect socket from room - O.S.
    socket.leave(lobbyCode);
    // Get new list of sockets in room - O.S.
    var socketsInRoom = await io.in(lobbyCode).fetchSockets();
    // Display user left room - O.S.
    console.log("User: " + socket.username + " left " + socket.data.room);
    console.log("\t Room count: " + socketsInRoom.length);
    // Format list to send back to clients- O.S.
    var users = getList(socketsInRoom);
    // Send list to clients still in room - O.S.
    io.to(socket.data.room).emit("new-user-response", users);
  });

  // Listens for a message from the client - O.S.
  socket.on("send_message", (data) => {
    // Emit the message back to the room clients are in - O.S.
    socket.to(data.room).emit("receive_message", data);
  });

  // Tell all users in same room to start game - O.S.
  socket.on("start-game", async (path) => {
    console.log("The Room - " + socket.data.room + " - has started a game");

    // Get list of players in the room - D.D.
    var socketsInRoom = await io.in(socket.data.room).fetchSockets();
    var listOfUsers = getList(socketsInRoom);
    // Construct input obj to pass to python process - D.D.
    const users_obj = {
      players: listOfUsers,
    };

    io.to(socket.data.room).emit("start-game", path);

    // Below are different python processes we can use to run when a game has started.

    // const python_process = spawner('python', ['server/game_constructs/testing.py'])
    // Start the python process, JSON.stringify to pass as valid JSON object. - D.D.
    // const python_process = spawner('python3', ['./script.py', JSON.stringify(users_obj)])
    const python_process = spawner("python", [
      "server/game_constructs/StartGame.py",
      JSON.stringify(users_obj),
    ]);
    // const python_process = spawner('python', ['server/game_constructs/testingInput.py'])
    // const python_process = spawner("python", ["server/game_constructs/TestingDiscardDeck.py"]);

    // Add current python process to list of python processes that are currently running - D.D.
    // NOTE: need to add function where if a room is empty, or if a client has left, then kill the process
    // and delete the process from the dictionary/list. - D.D.
    pythonProcesses[socket.data.room] = python_process;

    // only add one event listener for the python process - D.D.
    // Do all of the output parsing in this area, you can emit to specific clients - D.D.
    pythonProcesses[socket.data.room].stdout.on("data", function (data) {
      try {
        // this is how we'd compress data... we might use this later.
        // if we do, change the switch case to be jsonData['messageFlag']
        // and then change the io message to jsonData
        // const buffer = Buffer.from(data, 'binary');
        // const decompressedData = zlib.gunzipSync(buffer);
        // const jsonString = decompressedData.toString();
        // const jsonData = JSON.parse(jsonString)
        // console.log(jsonData)

        var jsonMessage = JSON.parse(data);
        io.to(socket.data.room).emit("valid-json", JSON.parse(data));

        switch (jsonMessage["messageFlag"]) {
          case "PLAYER-HAND":
            console.log(
              "Server Found Flag: Player-Hand, sending to: " +
                jsonMessage["socketID"]
            );
            io.to(jsonMessage["socketID"]).emit(
              "player-hand-update",
              JSON.parse(data)
            );
            break;

          case "PLAYER-BOARD":
            console.log("Server Found Flag: Player-Board Flag");
            io.to(socket.data.room).emit(
              "player-board-update",
              JSON.parse(data)
            );
            break;

          case "CHOICE":
            console.log("Server Found Flag: Choice Flag");
            io.to(jsonMessage["socketID"]).emit(
              "choice-update",
              JSON.parse(data)
            );
            break;

          case "SYSTEM":
            console.log("Server Found Flag: System Flag");
            io.to(socket.data.room).emit(
              "system-message-update",
              JSON.parse(data)
            );
            break;

          case "SYSTEM-PRIVATE":
            console.log("Server Found Flag: System Private Flag");
            io.to(jsonMessage["socketID"]).emit(
              "system-private-update",
              JSON.parse(data)
            );
            break;

          case "PLAYER-LIST":
            console.log("Server Found Flag: Player-List Flag");
            io.to(socket.data.room).emit(
              "player-list-update",
              JSON.parse(data)
            );
            break;

          case "DICE":
            console.log("Server Found Flag: Dice Flag");
            io.to(socket.data.room).emit("dice-update", JSON.parse(data));
            break;

          case "TREASURE":
            console.log("Server Found Flag: Treasure Flag");
            io.to(socket.data.room).emit("treasure-update", JSON.parse(data));
            break;

          case "MONSTER":
            console.log("Server Found Flag: Monster Flag");
            io.to(socket.data.room).emit("monster-update", JSON.parse(data));
            break;

          case "DISCARD-LOOT":
            console.log("Server Found Flag: Discard Loot Flag");
            io.to(socket.data.room).emit(
              "discard-loot-update",
              JSON.parse(data)
            );
            break;

          case "DISCARD-TREASURE":
            console.log("Server Found Flag: Discard Treasure Flag");
            io.to(socket.data.room).emit(
              "discard-treasure-update",
              JSON.parse(data)
            );
            break;

          case "DISCARD-MONSTER":
            console.log("Server Found Flag: Discard Monster Flag");
            io.to(socket.data.room).emit(
              "discard-monster-update",
              JSON.parse(data)
            );
            break;

          case "STACK":
            console.log("Server Found Flag: Stack Flag");
            io.to(socket.data.room).emit("stack-update", JSON.parse(data));
            break;

          default:
            console.log("Server Found Unknown Flag: " + data.toString());
            break;
        }
      } catch (e) {
        console.log(e);
      }
      console.log("Server received Python data: " + data.toString());
      io.to(socket.data.room).emit("from-python", data.toString());
    });

    // listen to errors from the game - D.D.
    pythonProcesses[socket.data.room].stderr.on("data", (data) => {
      console.error(data.toString());
    });
  });

  // Allow Users to access Game Board/Python Process commands. - D.D.
  socket.on("game-board-command", (data) => {
    const process = pythonProcesses[socket.data.room];

    socket.on("game-board-message", (data) => {
      console.log("Server Received Message: " + data);
      process.stdin.write(data + "\n");
      io.to(socket.data.room).emit("game-board-receive", "we received it");
    });
  });

  // Send a console log when a socket gets disconnected
  socket.on("disconnect", async (reason) => {
    totalClients = await io.fetchSockets();
    console.log("User disconnected from server");
    console.log("Reason: " + reason);
    console.log("TOTAL CLIENTS ON SERVER: " + totalClients.length);
  });
});

// Start the server to listen for communication
server.listen(PORT, () => {
  console.log("GAME SERVER IS RUNNING ON PORT " + PORT);
});
