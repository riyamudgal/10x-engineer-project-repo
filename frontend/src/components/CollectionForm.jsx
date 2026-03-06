import { useState } from "react";
import { createCollection } from "../api/api";

function CollectionForm({ refresh }) {

  const [name,setName] = useState("")
  const [description,setDescription] = useState("")

  const submit = async (e)=>{

    e.preventDefault()

    await createCollection({
      name,
      description
    })

    setName("")
    setDescription("")

    refresh()

  }

  return(

    <form onSubmit={submit}>

      <h2>Create Collection</h2>

      <div className="form-row">

        <label>Name</label>

        <input
          value={name}
          onChange={(e)=>setName(e.target.value)}
        />

      </div>

      <div className="form-row">

        <label>Description</label>

        <input
          value={description}
          onChange={(e)=>setDescription(e.target.value)}
        />

      </div>

      <button type="submit">
        Create Collection
      </button>

    </form>

  )

}

export default CollectionForm