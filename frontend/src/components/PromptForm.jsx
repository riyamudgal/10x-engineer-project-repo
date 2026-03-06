import { useState } from "react";
import { createPrompt } from "../api/api";

function PromptForm({ collections, refresh }) {

  const [title,setTitle] = useState("")
  const [content,setContent] = useState("")
  const [description,setDescription] = useState("")
  const [collectionId,setCollectionId] = useState("")

  const submit = async (e) => {

    e.preventDefault()

    await createPrompt({
      title,
      content,
      description,
      collection_id: collectionId || null
    })

    setTitle("")
    setContent("")
    setDescription("")
    setCollectionId("")

    refresh()
  }

  return(

    <form className="prompt-form" onSubmit={submit}>

      <h2>Create Prompt</h2>

      <div className="form-row">
        <label>Title</label>
        <input
          value={title}
          onChange={(e)=>setTitle(e.target.value)}
        />
      </div>

      <div className="form-row">
        <label>Content</label>
        <textarea
          value={content}
          onChange={(e)=>setContent(e.target.value)}
        />
      </div>

      <div className="form-row">
        <label>Description</label>
        <input
          value={description}
          onChange={(e)=>setDescription(e.target.value)}
        />
      </div>

      <div className="form-row">
        <label>Collection</label>

        <select
          value={collectionId}
          onChange={(e)=>setCollectionId(e.target.value)}
        >
          <option value="">No Collection</option>

          {collections.map(c => (
            <option key={c.id} value={c.id}>
              {c.name}
            </option>
          ))}
        </select>
      </div>

      <button type="submit">
        Create Prompt
      </button>

    </form>

  )
}

export default PromptForm