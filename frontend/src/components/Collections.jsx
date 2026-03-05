import { useState } from "react";
import { createCollection, deleteCollection } from "../api/api";

function Collections({ collections, refresh }) {

  const [name, setName] = useState("");

  const add = async () => {

    await createCollection({ name });

    setName("");

    refresh();
  };

  const remove = async (id) => {

    await deleteCollection(id);

    refresh();
  };

  return (
    <div className="sidebar">

      <h2>Collections</h2>

      {collections.map(c => (

        <div key={c.id}>

          {c.name}

          <button onClick={()=>remove(c.id)}>
            X
          </button>

        </div>

      ))}

      <input
        placeholder="New collection"
        value={name}
        onChange={(e)=>setName(e.target.value)}
      />

      <button onClick={add}>
        Add
      </button>

    </div>
  );
}

export default Collections;