import { deletePrompt } from "../api/api";

function Prompts({ prompts, collections, refresh }) {

  const getCollectionName = (id) => {
    const c = collections.find(col => col.id === id);
    return c ? c.name : "None";
  };

  const remove = async (id) => {
    await deletePrompt(id);
    refresh();
  };

  return (
    <div>

      <h2>Prompts</h2>

      {prompts.map(p => (

        <div key={p.id} className="card">

          <h3>{p.title}</h3>

          <p>{p.description}</p>

          <small>
            Collection: {getCollectionName(p.collection_id)}
          </small>

          <button onClick={() => remove(p.id)}>
            Delete
          </button>

        </div>

      ))}

    </div>
  );
}

export default Prompts;