export default {
  name: "listing",
  title: "Listing",
  type: "document",
  fields: [
    {
      name: "title",
      title: "Title",
      type: "string",
      validation: (Rule) => Rule.required(),
    },
    {
      name: "slug",
      title: "Slug",
      type: "slug",
      description: "Reserved for future detail pages — not used by the MVP listings grid yet.",
      options: {source: "title", maxLength: 96},
    },
    {
      name: "price",
      title: "Price",
      type: "number",
      validation: (Rule) => Rule.required(),
    },
    {
      name: "priceLabel",
      title: "Price Label",
      type: "string",
      description: 'Optional display override, e.g. "₹85L" or "₹25,000/mo". Falls back to a formatted price if left blank.',
    },
    {
      name: "locality",
      title: "Locality / Address",
      type: "string",
      validation: (Rule) => Rule.required(),
    },
    {
      name: "listingCategory",
      title: "Category",
      type: "string",
      options: {
        list: [
          {title: "Sale", value: "sale"},
          {title: "Rent", value: "rent"},
        ],
      },
      validation: (Rule) => Rule.required(),
    },
    {
      name: "propertyType",
      title: "Property Type",
      type: "string",
      options: {
        list: ["apartment", "house", "commercial", "land"],
      },
    },
    {
      name: "bedrooms",
      title: "Bedrooms",
      type: "number",
    },
    {
      name: "bathrooms",
      title: "Bathrooms",
      type: "number",
    },
    {
      name: "areaSqft",
      title: "Area (sqft)",
      type: "number",
    },
    {
      name: "description",
      title: "Description",
      type: "text",
    },
    {
      name: "images",
      title: "Images",
      type: "array",
      of: [{type: "image", options: {hotspot: true}}],
      validation: (Rule) => Rule.required().min(1),
    },
    {
      name: "status",
      title: "Status",
      type: "string",
      options: {
        list: ["available", "sold", "rented"],
      },
      initialValue: "available",
      validation: (Rule) => Rule.required(),
    },
    {
      name: "featured",
      title: "Featured",
      type: "boolean",
      description: "Reserved for a future homepage carousel — bubbles featured listings to the top of the grid today.",
      initialValue: false,
    },
    {
      name: "publishedAt",
      title: "Published At",
      type: "datetime",
      initialValue: () => new Date().toISOString(),
    },
  ],
  preview: {
    select: {
      title: "title",
      subtitle: "locality",
      media: "images.0",
    },
  },
};
