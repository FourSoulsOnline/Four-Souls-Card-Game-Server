/* Develper: Oscar Saavedra */

// Bring in express
import express from "express";
// Bring in the cors library
import cors from "cors";
// Create instance of HTTP library
import http from "http";
// Get the Server class from socket.io
import { Server } from "socket.io";

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
  socket.on("start-game", (path) => {
    io.to(socket.data.room).emit("start-game", path);
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
