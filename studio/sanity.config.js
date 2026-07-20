import {defineConfig} from "sanity";
import {structureTool} from "sanity/structure";
import {visionTool} from "@sanity/vision";
import {schemaTypes} from "./schemas";

// Must match the projectId/dataset used in site/js/listings.js.
const PROJECT_ID = "ortbv0xn";
const DATASET = "production";

export default defineConfig({
  name: "default",
  title: "Amber Consultants",
  projectId: PROJECT_ID,
  dataset: DATASET,
  plugins: [structureTool(), visionTool()],
  schema: {
    types: schemaTypes,
  },
});
