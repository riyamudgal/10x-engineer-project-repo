import { useEffect, useState } from "react";

import { fetchCollections } from "../api/api";

import Collections from "../components/Collections";
import CollectionForm from "../components/CollectionForm";

function CollectionsPage(){

  const [collections,setCollections] = useState([])

  const refresh = async ()=>{

    const res = await fetchCollections()

    setCollections(res.data.collections)

  }

  useEffect(()=>{

    async function load(){

      const res = await fetchCollections()

      setCollections(res.data.collections)

    }

    load()

  },[])

  return(

    <div className="page-layout">

      {/* LEFT PANEL */}

      <div className="left-panel">

        <Collections
          collections={collections}
          refresh={refresh}
        />

      </div>

      {/* RIGHT PANEL */}

      <div className="right-panel">

        <div className="create-card">

          <CollectionForm
            refresh={refresh}
          />

        </div>

      </div>

    </div>

  )

}

export default CollectionsPage