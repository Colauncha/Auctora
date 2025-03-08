import StepProgressBar from "react-step-progress";
import "react-step-progress/dist/index.css";
import { camera } from "../Constants";

const StepProgress = () => {
  return (
    <StepProgressBar
      startingStep={0}
      steps={[
        { label: "Description", image: camera },
        { label: "Categories" },
        { label: "Photos" },
        { label: "Delivery" },
      ]}
    />
  );
};

export default StepProgress;
