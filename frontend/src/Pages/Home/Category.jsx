// import { LuCrosshair } from "react-icons/lu";
import { NavLink } from "react-router-dom";
import CategoryCard from "../../Components/CategoryCard";
import {
  headphone,
  smartwatch,
  cellphone,
  computer,
  gamepad,
  camera,
} from "../../Constants";

const CategoryItemArr = [
  { _id: 1, icon: headphone, title: "headPhones", to: "/" },
  { _id: 2, icon: gamepad, title: "gaming", to: "/" },
  { _id: 3, icon: computer, title: "computers", to: "/" },
  { _id: 4, icon: cellphone, title: "phones", to: "/" },
  { _id: 5, icon: camera, title: "cameras", to: "/" },
  { _id: 6, icon: smartwatch, title: "appliances", to: "/" },
];

const Category = () => {
  return (
    <div className="formatter">
      <div className="border-t-[1px]  py-6 flex flex-col justify-center items-center">
        <h2 className="uppercase text-[24px] text-[#9f3247] font-[800] md:text-[48px] ">
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
              />
            );
          })}
        </div>
      </div>
    </div>
  );
};

export default Category;
