import express from "express";
import cors from "cors";
import dotenv from "dotenv";
import { readFileSync } from "fs";
import { fileURLToPath } from "url";
import { dirname } from "path";
import { getRecommendations } from "./recommendationEngine.js";

dotenv.config();

const app = express();
const PORT = process.env.PORT || 5000;

// Get current directory
const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

// Middleware
app.use(cors());
app.use(express.json());

// Load mock data
const mockData = JSON.parse(
  readFileSync(__dirname + "/mockData.json", "utf8")
);

// Route: Get all content
app.get("/api/content", (req, res) => {
  res.json(mockData.content);
});

// Route: Get recommendations based on user preferences
app.post("/api/recommendations", (req, res) => {
  const { preferences } = req.body;

  if (!preferences || preferences.length === 0) {
    return res
      .status(400)
      .json({ error: "Please provide at least one preference" });
  }

  const recommendations = getRecommendations(preferences, mockData.content);

  res.json({
    userPreferences: preferences,
    recommendations: recommendations,
    totalFound: recommendations.length,
  });
});

// Route: Health check
app.get("/", (req, res) => {
  res.json({ message: "Recommendation System API is running!" });
});

// Start server
app.listen(PORT, () => {
  console.log(`✅ Server running on http://localhost:${PORT}`);
  console.log(`📚 Content API: http://localhost:${PORT}/api/content`);
  console.log(
    `🎯 Recommendations API: POST http://localhost:${PORT}/api/recommendations`
  );
});
