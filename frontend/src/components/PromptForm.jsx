import { useState } from "react";
import { createPrompt } from "../api/api";

function PromptForm({ collections, refresh }) {

  const [title, setTitle] = useState("");
  const [content, setContent] = useState("");
  const [description, setDescription] = useState("");
  const [collectionId, setCollectionId] = useState("");

  const submit = async (e) => {

    e.preventDefault();

    await createPrompt({
      title,
      content,
      description,
      collection_id: collectionId || null
    });

    setTitle("");
    setContent("");
    setDescription("");
    setCollectionId("");

    refresh();
  };

  return (

    <form onSubmit={submit}>

      <h2>Create Prompt</h2>

      <input
        placeholder="Title"
        value={title}
        onChange={(e)=>setTitle(e.target.value)}
      />

      <textarea
        placeholder="Content"
        value={content}
        onChange={(e)=>setContent(e.target.value)}
      />

      <input
        placeholder="Description"
        value={description}
        onChange={(e)=>setDescription(e.target.value)}
      />

      <select
        value={collectionId}
        onChange={(e)=>setCollectionId(e.target.value)}
      >

        <option value="">
          No Collection
        </option>

        {collections.map(c => (
          <option key={c.id} value={c.id}>
            {c.name}
          </option>
        ))}

      </select>

      <button type="submit">
        Create Prompt
      </button>

    </form>

  );
}

export default PromptForm;