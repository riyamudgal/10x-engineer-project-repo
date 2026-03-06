import { useEffect, useState } from "react"

import { fetchCollections } from "../api/api"

import Collections from "../components/Collections"

function CollectionsPage(){

  const [collections,setCollections] = useState([])

  const refresh = async () => {

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

  <div className="container">

    <h1>Collections</h1>

    <div className="card-light">

      <Collections
        collections={collections}
        refresh={refresh}
      />

    </div>

  </div>

)
}

export default CollectionsPage