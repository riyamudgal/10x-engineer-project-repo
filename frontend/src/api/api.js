import axios from "axios";

const API = axios.create({
  baseURL: "https://automatic-eureka-xjw4xxrpqf69jj-8000.app.github.dev"
});

/* PROMPTS */

export const fetchPrompts = () =>
  API.get("/prompts");

export const createPrompt = (data) =>
  API.post("/prompts", data);

export const deletePrompt = (id) =>
  API.delete(`/prompts/${id}`);


/* COLLECTIONS */

export const fetchCollections = () =>
  API.get("/collections");

export const createCollection = (data) =>
  API.post("/collections", data);

export const deleteCollection = (id) =>
  API.delete(`/collections/${id}`);


/* STATS */

export const fetchStats = () =>
  API.get("/stats");