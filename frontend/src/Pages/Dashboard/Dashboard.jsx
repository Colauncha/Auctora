import BreadCrumb from "../../Components/Breadcrumbs";
import style from "./css/Dashboard.module.css"
import { useState, useEffect } from "react";
import Button from "../../Components/Button";
import { useNavigate } from "react-router-dom";
import { 
  Withdraw,
  WalletHistory,
  FundWallet,
  AddIcon,
  ActivityIcon,
  SettingsIcon,
  Logout,
  Edit,
  Money,
} from "../../Constants"
import Loader from "../../assets/loader";
import useAuthStore from "../../Store/AuthStore";
import { capitalize, currencyFormat, char20, links } from "../../utils";
import Avatar  from "./Avatar";


const Dashboard = () => {
  const [user, setUser] = useState({});
  const [displayName, setDisplayName] = useState("");
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();
  const logoutUser = useAuthStore((state) => state.logout);


  useEffect(() => {
    setLoading(true)
    const getUser = async () => { 
      let endpoint = `${links.local}users/profile`;
      try {
        const response = await fetch(endpoint, {
          method: "GET",
          credentials: "include",
        })
        if (response.ok) {
          let data = await response.json()
          setTimeout(() => {
            setUser(data.data)
            setDisplayName(data.data.username ? `@${capitalize(data.data.username)}` : data.data.email)
            setLoading(false)
            console.log(data.data)
          }, 1000)
        } else {
          let data = await response.json()
          console.error(data)
          navigate("/sign-in")
        }
      } catch (error) {
        console.log(error)
        navigate("/sign-in")
      }
    }
    getUser();
  }, [navigate])

  const logout = async () => {
    setLoading(true)
    let endpoint = `${links.local}users/logout`;

    try {
      const response = await fetch(endpoint, {
        method: "POST",
        credentials: "include",
      })
      if (response.ok) {
        let data = await response.json()
        console.log(data)
        setTimeout(() => {
          setLoading(false)
          logoutUser()
          localStorage.removeItem("token")
          localStorage.removeItem("userId")
          navigate("/")
        }, 500)

      } else {
        let data = await response.json()
        setLoading(false)
        console.error(data)
      }
    } catch (error) {
      setLoading(false)
      console.log(error)
    }
  }

  return (
    <>
      <div className={style.container}>
        <div className={style.sandwich}>
          <div className={style.avatar}>
            <Avatar imageUrl={user?.image ? user.image.public_url : null} username={user.username ? user.username : user.email} />
            <div className={style.avatarAfter}></div>
            <p>{char20(displayName)}</p>
            <p className={style.avatarEmail}>{user.username ? char20(user.email) : ''}</p>
          </div>
          <div className={style.actions}>
            <Button icon={AddIcon} className={style.button} iconClassName={style.buttonIcon} label="Create New" onClick={() => {}} />
            <Button icon={ActivityIcon} className={style.button} iconClassName={style.buttonIcon} label="Auctions" onClick={() => {}} />
            <Button icon={WalletHistory} className={style.button} iconClassName={style.buttonIcon} label="Wallet History" onClick={() => {}} />
          </div>
          <div className={style.preferences}>
            <Button icon={SettingsIcon} className={style.button} iconClassName={style.buttonIcon} label="Settings" onClick={() => {}} />
            <Button icon={Logout} className={style.button} iconClassName={style.buttonIcon} label="Logout" onClick={() => logout()} />
          </div>
        </div>
        <div className={style.panel}>
          <BreadCrumb />
          {loading && <Loader />}
          <div className={style.top}>
            <div className={style.greet}>
                <h1>Welcome back, {char20(displayName)}</h1>
                <div className="flex gap-3 flex-wrap">
                  <Button icon={Money} className={style.panelButton} iconClassName={style.buttonIcon} label="Account details" onClick={() => {}} />
                  <Button icon={Edit} className={style.panelButton} iconClassName={style.buttonIcon} label="Update profile" onClick={() => {}} />
                  <Button icon={AddIcon} className={style.panelButton} iconClassName={style.buttonIcon} label="Create Auction" onClick={() => {}} />
                  {/* <Button icon={FundWallet} className={style.panelButton} iconClassName={style.buttonIcon} label="Update profile" onClick={() => {}} /> */}
                </div>
            </div>
            <div className={style.wallet}>
              <h1>Wallet Balance</h1>
              <div className={style.walletBalance}>
                <p><span>Total:</span> {user.wallet ? currencyFormat(user.wallet) : currencyFormat("0.00")}</p>
                <p><span>Available:</span> {user.wallet ? currencyFormat(user.available_balance) : currencyFormat("0.00")}</p>
              </div>
              <div className={style.walletActions}>
                <Button icon={FundWallet} className={style.panelButton} iconClassName={style.buttonIcon} label="Fund Wallet" onClick={() => {}} />
                <Button icon={Withdraw} className={style.panelButton} iconClassName={style.buttonIcon} label="Withdraw" onClick={() => {}} />
              </div>
            </div>
          </div>
          <div className={style.bottom}>

          </div>
        </div>
      </div>
    </>
  );
}

export default Dashboard;