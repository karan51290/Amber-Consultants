import {defineCliConfig} from "sanity/cli";

const PROJECT_ID = "ortbv0xn";
const DATASET = "production";

export default defineCliConfig({
  api: {
    projectId: PROJECT_ID,
    dataset: DATASET,
  },
  studioHost: "amber-consultants",
});
