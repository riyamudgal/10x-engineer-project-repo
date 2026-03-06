import { NavLink } from "react-router-dom";

function Navbar(){

  return(

    <div className="navbar">

      <div className="logo">PromptLab</div>

      <div className="nav-links">

        <NavLink
          to="/"
          className={({isActive}) =>
            isActive ? "nav-btn active" : "nav-btn"
          }
        >
          Dashboard
        </NavLink>

        <NavLink
          to="/prompts"
          className={({isActive}) =>
            isActive ? "nav-btn active" : "nav-btn"
          }
        >
          Prompts
        </NavLink>

        <NavLink
          to="/collections"
          className={({isActive}) =>
            isActive ? "nav-btn active" : "nav-btn"
          }
        >
          Collections
        </NavLink>

      </div>

    </div>

  )

}

export default Navbar