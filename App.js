const express = require("express");
const mongoose = require("mongoose");
const bodyParser = require("body-parser");
const cookieParser = require("cookie-parser");
const bcrypt = require("bcrypt");

const app = express();

app.use(express.json());
app.use(cookieParser());

// MongoDb Connection

mongoose
  .connect("mongodb://localhost:27017/register_login", {
    useNewUrlParser: true,
    useUnifiedTopology: true,
  })
  .then(() => {
    console.log("MongoDB Connected");
  })
  .catch((error) => {
    console.log("Conection error");
  });

// Schema

const userSchema = new mongoose.Schema({
  userName: String,
  password: String,
});

const user = mongoose.model("User", userSchema);

//Routes

app.post("/api/register", async (req, res) => {
  try {
    const { userName, password } = req.body;
    const hashedPassword = await bcrypt.hash(password, 10);
    const newUser = new user({
      userName,
      password: hashedPassword,
    });
    await newUser.save();
    res.json({ message: "User Registered" });
  } catch (error) {
    res.status(500).send("error");
  }
});

app.post("/api/login", async (req, res) => {
  try {
    const { userName, password } = req.body;
    const User = await user.findOne({ userName });

    if (User && (await bcrypt.compare(password, User.password))) {
      res.cookie("userToken", User._id.toString(), { httpOnly: true });
      res.status(200).send("Login Success");
    } else {
      res.status(401).send("Invalid Credentials");
    }
  } catch (error) {
    res.status(500).send("error");
  }
});

const PORT = process.env.PORT || 5000;

app.listen(PORT, () => {
  console.log(`Server is running on port ${PORT}`);
});
