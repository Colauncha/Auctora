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
import { capitalize, currencyFormat, charLimit, current } from "../../utils";
import Avatar  from "./Avatar";


const Dashboard = () => {
  const [user, setUser] = useState({});
  const [displayName, setDisplayName] = useState("");
  const [loading, setLoading] = useState(false);
  const [auctions, setAuctions] = useState([]);
  const navigate = useNavigate();
  const logoutUser = useAuthStore((state) => state.logout);


  useEffect(() => {
    setLoading(true)

    const getUser = async () => { 
      let endpoint = `${current}users/profile`;
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
            setAuctions(data.data.auctions)
            setLoading(false)
            sessionStorage.setItem('_user', JSON.stringify(data.data))
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
    let data = JSON.parse(sessionStorage.getItem('_user'))
    if (!data) {
      getUser();
      return
    } else {
      setUser(data);
      setDisplayName(data.username ? `@${capitalize(data.username)}` : data.email);
      setAuctions(data.auctions);
      setLoading(false);
      return;
    }
  }, [navigate])

  const logout = async () => {
    setLoading(true)
    let endpoint = `${current}users/logout`;

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
          sessionStorage.removeItem('_user')
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

  const viewAuction = async (id) => {
    console.log(id)
  }

  return (
    <>
      <div className={style.container}>
        <div className={style.sandwich}>
          <div className={style.avatar}>
            <Avatar imageUrl={user?.image ? user.image.public_url : null} username={user.username ? user.username : user.email} />
            <div className={style.avatarAfter}></div>
            <p>{charLimit(displayName, 20)}</p>
            <p className={style.avatarEmail}>{user.username ? charLimit(user.email, 20) : ''}</p>
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
                <h1>Welcome back, {charLimit(displayName, 20)}</h1>
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
                        <div className={style.bottomLeft}>
                          {loading ?? <Loader />}
                          {
                          auctions.length > 0 ? (
                            <>
                            <h1>Your Auctions <span onClick={() => {}}>View all</span></h1>
                            <table className={style.auctionTable}>
                              <thead>
                                <tr>
                                <th>Name</th>
                                <th>Description</th>
                                <th>Start price</th>
                                <th>Current price</th>
                                <th>Status</th>
                                </tr>
                              </thead>
                              <tbody>
                                {auctions.map((obj) => (
                                  <tr key={obj.id} onClick={() => viewAuction(obj.id)}>
                                  <td className="relative group">
                                    {charLimit(obj.item[0].name, 10)}
                                    <span className="absolute left-0 bottom-full mb-1 hidden w-max bg-gray-700 text-white text-xs rounded py-1 px-2 group-hover:block">
                                    {obj.item[0].name}
                                    </span>
                                  </td>
                                  <td className="relative group">
                                    {charLimit(obj.item[0].description, 20)}
                                    <span className="absolute left-0 bottom-full mb-1 hidden w-max bg-gray-700 text-white text-xs rounded py-1 px-2 group-hover:block">
                                    {obj.item[0].description}
                                    </span>
                                  </td>
                                  <td className="relative group">
                                    {currencyFormat(obj.start_price)}
                                    <span className="absolute left-0 bottom-full mb-1 hidden w-max bg-gray-700 text-white text-xs rounded py-1 px-2 group-hover:block">
                                    {currencyFormat(obj.start_price)}
                                    </span>
                                  </td>
                                  <td className="relative group">
                                    {currencyFormat(obj.current_price)}
                                    <span className="absolute left-0 bottom-full mb-1 hidden w-max bg-gray-700 text-white text-xs rounded py-1 px-2 group-hover:block">
                                    {currencyFormat(obj.current_price)}
                                    </span>
                                  </td>
                                  <td className="relative group">
                                    {capitalize(obj.status)}
                                    <span className="absolute left-0 bottom-full mb-1 hidden w-max bg-gray-700 text-white text-xs rounded py-1 px-2 group-hover:block">
                                    {capitalize(obj.status)}
                                    </span>
                                  </td>
                                  </tr>
                                ))}
                              </tbody>
                            </table>
                            {/* <Button label="View All" className={`${style.panelButton} ${style.bottomLeftButton}`} onClick={() => {}} /> */}
                  </>
                ) : (
                <>
                  <h2>No Auctions yet</h2>
                  <Button icon={AddIcon} className={style.panelButton} iconClassName={style.buttonIcon} label="Create Auction" onClick={() => {}} />
                </>
              )
              }
            </div>
            <div className={style.bottomRight}>
              <div className={style.bottomRightRating}>
                <p>Ratings</p>
              </div>
              <div className={style.bottomRightBids}>
                <p>Bids</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </>
  );
}

export default Dashboard;