import BreadCrumb from "../../Components/Breadcrumbs";
import style from "./css/Dashboard.module.css"
import { useState, useEffect } from "react";


const Dashboard = () => {
  const [user, setUser] = useState({});


  useEffect(() => {
    const getUser = async () => { 
      let endpoint = "https://api-auctora.vercel.app/api/users";
      // let endpoint = "http://localhost:8000/api/users";
      try {
        const response = await fetch(endpoint, {
          method: "GET",
          credentials: "include",
          // headers: {
          //  'Content-Type':'application/json',
          // },
        })
        if (response.ok) {
          let data = await response.json()
          setUser(data.data)
          console.log(data.data)
        } else {
          let data = await response.json()
          console.error(data)
        }
      } catch (error) {
        console.log(error)
      }
    }
    getUser();
  }, [])

  return (
    <>
      <div className={style.container}>
        <div className={style.sandwich}>
          <ul>
            <li>Option 1</li>
            <li>Option 2</li>
          </ul>
        </div>
        <div className={style.panel}>
          <BreadCrumb />
          {}
        </div>
      </div>
    </>
  );
}

export default Dashboard;