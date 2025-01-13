import { Link, NavLink } from "react-router-dom";
import { useNavigate } from "react-router-dom";

import Search from "../../Components/Search";
import { likee, logo, search_glass, user } from "../../Constants";
import { useEffect, useState, useCallback } from "react";
import { LuAlignJustify } from "react-icons/lu";
import { RiCloseLargeFill } from "react-icons/ri";
import useModeStore from "../../Store/Store";

const Nav = () => {
  const menuArr = [
    { _id: 1, label: "Home", link: "/" },
    { _id: 2, label: "Auctlist", link: "/list" },
    { _id: 3, label: "About Us", link: "/about-us" },
  ];

  const {} = useModeStore();
  const [isMobile, setIsMobile] = useState(window.innerWidth <= 768);
  const [isMenuOpen, setIsMenuOpen] = useState(false);

  const updateIsMobile = useCallback(() => {
    setIsMobile(window.innerWidth <= 768);
  }, []);

  const toggleMenu = () => {
    setIsMenuOpen((prev) => !prev);
  };

  useEffect(() => {
    window.addEventListener("resize", updateIsMobile);
    return () => {
      window.removeEventListener("resize", updateIsMobile);
    };
  }, [updateIsMobile]);

  const navigate = useNavigate();
  const signIn = () => {
    navigate("/sign-in");
  };

  const handleSearch = () => {
    console.log("searching...");
  };

  return (
    <div className="h-[36px] my-[20px]">
      {isMobile ? (
        <div className="formatter flex justify-between items-center">
          <div className="flex items-center gap-4 relative">
            {isMenuOpen ? (
              <RiCloseLargeFill
                size={30}
                onClick={toggleMenu}
                className="cursor-pointer"
              />
            ) : (
              <LuAlignJustify
                size={30}
                onClick={toggleMenu}
                className="cursor-pointer"
              />
            )}
            <Link to={`/`}>
              <img src={logo} alt="logo" className="w-[130px]" />
            </Link>
          </div>
          {isMenuOpen && (
            <nav className="text-[16px] absolute z-10 text-white bg-gradient-to-r from-[#7B2334] to-[#9F3247] left-0 top-0 w-full p-10">
              <ul className="flex flex-col gap-8 pb-10 m-auto">
                {menuArr.map((item) => (
                  <NavLink key={item._id} to={item.link} onClick={toggleMenu}>
                    {item.label}
                  </NavLink>
                ))}
              </ul>
              <div className="flex gap-4 mr-auto">
                <Search
                  img={search_glass}
                  placeholder={`Search for Products`}
                  onClick={handleSearch}
                />
                <RiCloseLargeFill
                  size={40}
                  className="cursor-pointer"
                  onClick={toggleMenu}
                />
              </div>
            </nav>
          )}
          <div className="flex gap-4">
            <img src={search_glass} alt="" className="h-4 w-4 cursor-pointer" />
            <img src={likee} alt="" className="h-4 w-4 cursor-pointer" />
            <img src={user} alt="" className="h-4 w-4 cursor-pointer" />
          </div>
        </div>
      ) : (
        <div className="formatter flex justify-between items-center">
          <Link to={`/`}>
            <img src={logo} alt="logo" className="w-[130px]" />
          </Link>
          <nav className="sm:text-[15px] text-[16px]">
            <ul className="flex gap-8">
              {menuArr.map((item) => (
                <NavLink key={item._id} to={item.link}>
                  {item.label}
                </NavLink>
              ))}
            </ul>
          </nav>
          <Search
            className={`sm:w-[200px] lg:w-[360px] xl:w-[650px]`}
            img={search_glass}
            onClick={handleSearch}
            placeholder={`Search for products...`}
          />
          <div className="flex gap-4">
            <img src={likee} alt="" className="h-4 w-4 cursor-pointer" />
            <img
              src={user}
              alt=""
              className="h-4 w-4 cursor-pointer"
              onClick={signIn}
            />
          </div>
        </div>
      )}
    </div>
  );
};

export default Nav;
