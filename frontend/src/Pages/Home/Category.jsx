// import { LuCrosshair } from "react-icons/lu";
import { NavLink } from "react-router-dom";
import CategoryCard from "../../Components/CategoryCard";
import useModeStore from "../../Store/Store";
import {
  headphone,
  smartwatch,
  cellphone,
  computer,
  gamepad,
  camera,
  dcamera,
  dcomputer,
  dgaming,
  dheadphone,
  dphone,
  dsmartwatch,
} from "../../Constants";

const Category = () => {
  const { isMobile } = useModeStore();
  const CategoryItemArr = [
    {
      _id: 1,
      icon: isMobile ? headphone : dheadphone,
      title: "headPhones",
      to: "/category",
    },
    {
      _id: 2,
      icon: isMobile ? gamepad : dgaming,
      title: "gaming",
      to: "/category",
    },
    {
      _id: 3,
      icon: isMobile ? computer : dcomputer,
      title: "computers",
      to: "/category",
    },
    {
      _id: 4,
      icon: isMobile ? cellphone : dphone,
      title: "phones",
      to: "/category",
    },
    {
      _id: 5,
      icon: isMobile ? camera : dcamera,
      title: "cameras",
      to: "/category",
    },
    {
      _id: 6,
      icon: isMobile ? smartwatch : dsmartwatch,
      title: "appliances",
      to: "/category",
    },
  ];

  return (
    <div className="formatter">
      <div className="border-t-[1px]  py-6 flex flex-col justify-center items-center">
        <h2 className="uppercase text-[24px] text-[#9f3247] font-[800] md:text-[32px] ">
          Browse by Categories
        </h2>
        <div className="grid grid-cols-3 gap-5 lg:gap-10 mt-10">
          {CategoryItemArr.map((item) => {
            return (
              <CategoryCard
                key={item._id}
                icon={item.icon}
                title={item.title}
                className={`cursor-pointer hover:border-[1px] hover:bg-[#9f324826]`}
                to={`/category`}
              />
            );
          })}
        </div>
      </div>
    </div>
  );
};

export default Category;
