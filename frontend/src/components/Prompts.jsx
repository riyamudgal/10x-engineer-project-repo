import { deletePrompt } from "../api/api";

function Prompts({prompts, collections, refresh}){

  const getCollectionName = (id) => {

    const c = collections.find(x => x.id === id)

    return c ? c.name : "None"
  }

  const remove = async (id) => {

    await deletePrompt(id)

    refresh()

  }

  return(

    <>
      {prompts.map(p => (

        <div key={p.id} className="prompt-card">

          <h3>{p.title}</h3>

          <p>{p.content}</p>

          {p.description && (
            <p className="prompt-desc">
              {p.description}
            </p>
          )}

          <small>
            Collection: {getCollectionName(p.collection_id)}
          </small>

          <button
            className="delete-btn"
            onClick={()=>remove(p.id)}
          >
            Delete
          </button>

        </div>

      ))}
    </>
  )
}

export default Prompts