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

  return (

  <div className="page-layout">

    {/* LEFT PANEL */}

    <div className="left-panel">

      <Prompts
        prompts={prompts}
        collections={collections}
        refresh={refresh}
      />

    </div>


    {/* RIGHT PANEL */}

    <div className="right-panel">

      <div className="create-card">

        <PromptForm
          collections={collections}
          refresh={refresh}
        />

      </div>

    </div>

  </div>

)
}

export default PromptsPage