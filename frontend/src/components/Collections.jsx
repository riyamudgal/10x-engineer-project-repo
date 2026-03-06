import { useState } from "react"
import { deleteCollection } from "../api/api"

function Collections({collections, refresh}){

  const [selected,setSelected] = useState([])

  const toggleSelect = (id)=>{

    if(selected.includes(id)){
      setSelected(selected.filter(x=>x!==id))
    }
    else{
      setSelected([...selected,id])
    }

  }

  const deleteSelected = async ()=>{

    for(let id of selected){
      await deleteCollection(id)
    }

    setSelected([])

    refresh()

  }

  return(

    <div>

      {selected.length>0 &&(

        <button
          className="delete-selected"
          onClick={deleteSelected}
        >
          Delete Selected
        </button>

      )}

      {collections.map(c=>(

        <div key={c.id} className="prompt-row">

          <div className="prompt-header">

            <input
              type="checkbox"
              checked={selected.includes(c.id)}
              onChange={()=>toggleSelect(c.id)}
            />

            <span>{c.name}</span>

          </div>

        </div>

      ))}

    </div>

  )

}

export default Collections