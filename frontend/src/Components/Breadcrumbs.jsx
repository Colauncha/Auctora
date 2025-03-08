import { useLocation } from "react-router-dom";
import style from "./css/Breadcrumbs.module.css";

const capitalize = (s) => s.charAt(0).toUpperCase() + s.slice(1);

const BreadCrumb = () => {
  const location = useLocation();
  const pathnames = location.pathname.split("/").filter((x) => x);

  return (
    <div className={`breadcrumb ${style.text}`}>
      <div className="breadcrumb_item">
        <a href="/">Home</a>
        {pathnames.map((name, index) => {
          // Generate the route path for each breadcrumb
          const routeTo = `/${pathnames.slice(0, index + 1).join("/")}`;
          const isLast = index === pathnames.length - 1;
          return isLast ? (
            <span key={name}>&nbsp;&gt;&nbsp;{capitalize(name)}</span>
          ) : (
            <span key={name}>
              &nbsp;&gt;&nbsp;<a href={routeTo}>{capitalize(name)}</a>
            </span>
          );
        })}
      </div>
    </div>
  );
};

export default BreadCrumb;
