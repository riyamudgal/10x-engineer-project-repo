import axios from "axios";

const API = axios.create({
  baseURL: "http://127.0.0.1:8000"
});

/* PROMPTS */

export const fetchPrompts = (collectionId, search) =>
  API.get("/prompts", {
    params: { collection_id: collectionId, search }
  });

export const createPrompt = (data) =>
  API.post("/prompts", data);

export const updatePrompt = (id, data) =>
  API.put(`/prompts/${id}`, data);

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