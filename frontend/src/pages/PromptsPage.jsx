import { useEffect, useState } from "react";
import { fetchPrompts, fetchCollections } from "../api/api";

import PromptForm from "../components/PromptForm";
import Prompts from "../components/Prompts";

function PromptsPage(){

  const [prompts,setPrompts] = useState([])
  const [collections,setCollections] = useState([])

  const refresh = async () => {

    const p = await fetchPrompts()
    const c = await fetchCollections()

    setPrompts(p.data.prompts)
    setCollections(c.data.collections)

  }

  useEffect(()=>{

    async function load(){

      const p = await fetchPrompts()
      const c = await fetchCollections()

      setPrompts(p.data.prompts)
      setCollections(c.data.collections)

    }

    load()

  },[])

  return(

  <div className="container">

    <h1>Prompts</h1>

    {/* CREATE PROMPT CENTER CARD */}

    <div className="create-prompt card-light">

      <PromptForm
        collections={collections}
        refresh={refresh}
      />

    </div>

    {/* PROMPT GRID */}

    <div className="prompts-grid">

      <Prompts
        prompts={prompts}
        collections={collections}
        refresh={refresh}
      />

    </div>

  </div>

)
}

export default PromptsPage