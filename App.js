const express = require("express");
const mongoose = require("mongoose");
const bodyParser = require("body-parser");
const cookieParser = require("cookie-parser");
const bcrypt = require("bcrypt");
const axios = require("axios");
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
  phoneNumber: String,
  email: String,
});

const user = mongoose.model("User", userSchema);
const API_KEY = "6db423635db56cd0fdf46cce1c5edfb3";
const APP_ID = "750c3845";

//Routes

app.get("/api/food_search", async (req, res) => {
  const { ingr, brand } = req.query;
  console.log(ingr, brand);

  try {
    const response = await axios.get(
      `https://api.edamam.com/api/food-database/v2/parser?app_id=750c3845&app_key=6db423635db56cd0fdf46cce1c5edfb3&ingr=${ingr}&brand=${brand}&nutrition-type=logging`
    );
    console.log(response.data.hints);
    res.send(response.data.hints);
  } catch (error) {
    console.error(error);
  }
});

app.post("/api/food_request_nutrients", async (req, res) => {
  const { quantity, measureURI, qualifiers, foodId } = req.body.ingredients[0];

  const recipe = {
    ingredients: [
      {
        quantity,
        measureURI,
        qualifiers,
        foodId,
      },
    ],
  };

  try {
    const response = await axios.post(
      `https://api.edamam.com/api/food-database/v2/nutrients?app_id=${APP_ID}&app_key=${API_KEY}`,
      recipe,
      {
        headers: {
          "Content-Type": "application/json",
        },
      }
    );

    res.json(response.data);
  } catch (error) {
    console.error(error);
    res.status(500).json({ error: error.message });
  }
});

// https://api.edamam.com/api/nutrition-data?app_id=b25bef67&app_key=9116481b7e44b86ff4e673852e47d334&nutrition-type=cooking&ingr=5%20rice'

app.post("/api/register", async (req, res) => {
  try {
    const { userName, password, phoneNumber, email } = req.body;
    const hashedPassword = await bcrypt.hash(password, 10);
    const newUser = new user({
      userName,
      password: hashedPassword,
      phoneNumber,
      email,
    });
    await newUser.save();
    res.json({ message: "User Registered" });
  } catch (error) {
    res.status(500).send("error");
  }
});

app.post("/api/login", async (req, res) => {
  try {
    const { userName, password, phoneNumber, email } = req.body;
    const User = await user.findOne({ email });

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
