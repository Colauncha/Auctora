import Spotlight from "../Spotlight";
import Separator from "../../../Components/Separator";
import Category from "../Category";
import Wrapper from "../../../Components/Wrapper";

const Layout = () => {
  return (
    <div>
      <Spotlight />
      <Separator title={`ONGOING AUCTIONS`} />
      <Wrapper />
      <Category />
    </div>
  );
};

export default Layout;
