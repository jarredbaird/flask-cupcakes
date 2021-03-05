BASE_URL = "http://localhost:5000/api";

function generateCupcardCard(cupcake) {
  return `
        <div class="col" data-cc-id=${cupcake.cc_id}>
          <div class="card">
            <img src="${cupcake.image}" class="card-img-top" alt="${cupcake.flavor}">
            <div class="card-body">
              <h5 class="card-title">${cupcake.flavor}</h5>
              <p class="card-text">Size: ${cupcake.size}</p>
              <p class="card-text">Rating: ${cupcake.rating}</p>
              <button type="button" 
                      class="btn btn-danger"
                      id="delete-${cupcake.cc_id}>Delete</button>
            </div>
          </div>
        </div>`;
}

async function displayCupcakeCards() {
  const response = await axios.get(`${BASE_URL}/cupcakes`);
  for (let cc of response.data.cupcakes) {
    let newCupcake = $(generateCupcakeHTML(cc));
    $("#cc-cards").append(newCupcake);
  }
  $("#cc-cards").append("<button id='to_list'>Back to list</button>");
  debugger;
}

function toggleListAndForm() {
  $("#list").toggle();
  $("#form").toggle();
}

$("#to-list").on("submit", (e) => {
  e.preventDefault();
  toggleListAndForm();
});

$("#to-add").on("submit", (e) => {
  e.preventDefault();
  toggleListAndForm();
});

$("#form").on("submit", async function (e) {
  e.preventDefault();

  let flavor = $("#form-flavor").val();
  let rating = $("#form-rating").val();
  let size = $("#form-size").val();
  let image = $("#form-image").val();

  const response = await axios.post(`${BASE_URL}/cupcakes`, {
    flavor,
    rating,
    size,
    image,
  });

  let cc = $(generateCupcardCard(response.data.cupcake));
  $("#cc-cards").append(cc);
});

$("#list").on("click", ".btn-danger", async function (e) {
  e.preventDefault();
  let $cupcake = $(e.target).closest(".col");
  let cc_id = $cupcake.attr("data-cc-id");

  await axios.delete(`${BASE_URL}/cupcakes/${cc_id}`);
  $cupcake.remove;
});

$(displayCupcakeCards);
