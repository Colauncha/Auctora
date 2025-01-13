import { LuCrosshair } from "react-icons/lu";
import CategoryCard from "../../Components/CategoryCard";

const CategoryItemArr = [
  { _id: 1, icon: <LuCrosshair />, title: "headPhones" },
  { _id: 2, icon: <LuCrosshair />, title: "gaming" },
  { _id: 3, icon: <LuCrosshair />, title: "computers" },
  { _id: 4, icon: <LuCrosshair />, title: "phones" },
  { _id: 5, icon: <LuCrosshair />, title: "cameras" },
  { _id: 6, icon: <LuCrosshair />, title: "appliances" },
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
