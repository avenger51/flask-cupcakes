const BASE_URL = "http://127.0.0.1:5000/api"; 

function createCupcakeForm(cupcake) {
    return `
  <div data-cupcake-id=${cupcake.id}>
    <li>
      ${cupcake.flavor} / ${cupcake.size} / ${cupcake.rating}
      <button class="delete-button">X</button>
    </li>
    <img class="Cupcake-img"
          src="${cupcake.image}"
          alt="(no image provided)">
  </div>
`;

}

//$('.new-cupcake-form').click(showAllCupcakes) 

async function showInitialCupcakes() {
  const response = await axios.get(`${BASE_URL}/cupcakes`);  //waiting for: @app.route("/api/cupcakes", methods=['GET'])

  for (let cupcakeData of response.data.cupcakes) {
    let newCupcake = $(createCupcakeForm(cupcakeData));
    $("#cupcakes-list").append(newCupcake);
  }
}
$("#new-cupcake-form").on("submit", async function (evt) {
  evt.preventDefault();

  let flavor = $("#form-flavor").val();
  let rating = $("#form-rating").val();
  let size = $("#form-size").val();
  let image = $("#form-image").val();

  const newCupcakeResponse = await axios.post(`${BASE_URL}/cupcakes`, {
    flavor,
    rating,
    size,
    image
  });

  let newCupcake = $(generateCupcakeHTML(newCupcakeResponse.data.cupcake));
  $("#cupcakes-list").append(newCupcake);
  $("#new-cupcake-form").trigger("reset");
});




$("#cupcakes-list").on("click", ".delete-button", async function (evt) {
  evt.preventDefault();
  let $cupcake = $(evt.target).closest("div");
  let cupcakeId = $cupcake.attr("data-cupcake-id");

  await axios.delete(`${BASE_URL}/cupcakes/${cupcakeId}`);
  $cupcake.remove();
});

$(showInitialCupcakes); //remember to call it...

