// One-off script to seed a few test listings for end-to-end verification.
// Run with: npx sanity exec scripts/seed-test-listings.js --with-user-token
const {getCliClient} = require("sanity/cli");
const fs = require("node:fs");
const path = require("node:path");

const IMAGES_DIR = path.resolve(__dirname, "../../site/assets/images");

const client = getCliClient();

const LISTINGS = [
  {
    title: "Modern 3BHK Villa with Private Pool",
    price: 8500000,
    priceLabel: "₹85L",
    locality: "ECR, Chennai",
    propertyType: "house",
    bedrooms: 3,
    bathrooms: 3,
    areaSqft: 2200,
    description: "A modern 3BHK villa with a private pool, landscaped garden, and covered parking on ECR.",
    status: "available",
    featured: true,
    image: "modern-house-facade-2021-08-27-19-27-44--1024x683.jpg",
  },
  {
    title: "Spacious 2BHK Apartment for Rent",
    price: 25000,
    priceLabel: "₹25,000/mo",
    locality: "Choolaimedu, Chennai",
    propertyType: "apartment",
    bedrooms: 2,
    bathrooms: 2,
    areaSqft: 1150,
    description: "Well-ventilated 2BHK apartment close to schools and public transport in Choolaimedu.",
    status: "available",
    featured: false,
    image: "residential.jpg",
  },
  {
    title: "Independent House — Ready to Move",
    price: 12000000,
    priceLabel: "₹1.2 Cr",
    locality: "Anna Nagar, Chennai",
    propertyType: "house",
    bedrooms: 4,
    bathrooms: 3,
    areaSqft: 2800,
    description: "Four-bedroom independent house in Anna Nagar. Included to verify sold listings are excluded from the public grid.",
    status: "sold",
    featured: false,
    image: "big-image-of-house-keys-1024x683.jpg",
  },
];

async function run() {
  for (const listing of LISTINGS) {
    const imagePath = path.join(IMAGES_DIR, listing.image);
    console.log(`Uploading image for "${listing.title}"...`);
    const asset = await client.assets.upload("image", fs.createReadStream(imagePath), {
      filename: listing.image,
    });

    const doc = {
      _type: "listing",
      title: listing.title,
      price: listing.price,
      priceLabel: listing.priceLabel,
      locality: listing.locality,
      propertyType: listing.propertyType,
      bedrooms: listing.bedrooms,
      bathrooms: listing.bathrooms,
      areaSqft: listing.areaSqft,
      description: listing.description,
      status: listing.status,
      featured: listing.featured,
      publishedAt: new Date().toISOString(),
      images: [
        {
          _type: "image",
          _key: "img1",
          asset: {_type: "reference", _ref: asset._id},
        },
      ],
    };

    const created = await client.create(doc);
    console.log(`Created listing "${created.title}" (${created._id})`);
  }
}

run().catch((err) => {
  console.error(err);
  process.exit(1);
});
