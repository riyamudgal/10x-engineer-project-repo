import { useState } from "react";
import { createCollection, deleteCollection } from "../api/api";

function Collections({ collections, refresh }) {

  const [name, setName] = useState("");
  const [description, setDescription] = useState("");

  const addCollection = async () => {

    try {

      await createCollection({
        name: name,
        description: description
      });

      setName("");
      setDescription("");

      refresh();

    } catch (err) {
      console.error("Collection error:", err);
    }
  };

  return (
    <div className="sidebar">

      <h2>Collections</h2>

      {collections.map(c => (
        <div key={c.id}>
          <b>{c.name}</b>

          {c.description && (
            <p style={{fontSize:"12px"}}>{c.description}</p>
          )}

          <button onClick={()=>deleteCollection(c.id)}>
            X
          </button>
        </div>
      ))}

      <input
        placeholder="Collection name"
        value={name}
        onChange={(e)=>setName(e.target.value)}
      />

      <input
        placeholder="Description"
        value={description}
        onChange={(e)=>setDescription(e.target.value)}
      />

      <button onClick={addCollection}>
        Add
      </button>

    </div>
  );
}

export default Collections;