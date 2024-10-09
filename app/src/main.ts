import axios from "axios";

type ImageMetaData = {
  image_path: string;
  application_name: string;
  timestamp: string;
  distance: number;
};

const fetch_top_results = async (
  text_query: string,
): Promise<ImageMetaData[]> => {
  const res = await axios(
    `http://localhost:8000/search?text_query=${text_query}`,
  );

  console.log(res.data);
  const results: ImageMetaData[] = res.data.image_list_with_metadata;
  return results;
};

const image_gallery: HTMLElement | null =
  document.querySelector("#image-gallery");

const render_image_gallery = (results: ImageMetaData[]) => {
  if (!image_gallery) return;

  image_gallery.innerHTML = "";

  results.forEach((result) => {
    const image_container = document.createElement("div");
    image_container.classList.add("image-container");

    const image = document.createElement("img");
    //WARN: Fix this image path
    image.src = "../../server/" + result.image_path;
    image.alt = result.application_name;
    image.classList.add("image");

    const metadata_container = document.createElement("div");
    metadata_container.classList.add("metadata-container");

    const app_name = document.createElement("p");
    app_name.textContent = `App: ${result.application_name ? result.application_name : "Unknown"}`;
    metadata_container.appendChild(app_name);

    const timestamp = document.createElement("p");
    timestamp.textContent = `Timestamp: ${result.timestamp}`;
    metadata_container.appendChild(timestamp);

    const distance = document.createElement("p");
    distance.textContent = `Distance: ${result.distance}`;
    metadata_container.appendChild(distance);

    image_container.appendChild(image);
    image_container.appendChild(metadata_container);

    image_gallery.appendChild(image_container);
  });
};

const search_btn: HTMLElement | null = document.querySelector("#search-icon");

search_btn?.addEventListener("click", async () => {
  const text_query = (
    document.querySelector("#search-input") as HTMLInputElement
  ).value;
  if (!text_query) {
    //TODO: Add a better error message
    alert("Please enter a search query");
    return;
  }
  const results = await fetch_top_results(text_query);
  render_image_gallery(results);
});
