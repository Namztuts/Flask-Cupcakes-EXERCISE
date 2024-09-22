const BASE_URL = '/api/cupcakes';
const $cupcakesList = $('.cupcakes-list');
const $cupcakeForm = $('.cupcake-form');

//function for creating the HTML to add to the DOM
function addCupcakeHTML(cupcake) {
   const $cupcakeDiv = $('<div>').attr('data-id', cupcake.id);
   const $cupcakeImg = $('<img>')
      .attr('src', cupcake.image)
      .attr('alt', `A ${cupcake.flavor} flavored cupcake`);
   const $cupcakeLi = $('<li>').text(
      `Flavor: ${cupcake.flavor} | Size: ${cupcake.size} | Rating: ${cupcake.rating}`
   );
   const $deleteButton = $('<button>').addClass('delete-cupcake').text('X');

   $cupcakeLi.append($deleteButton);
   $cupcakeDiv.append($cupcakeImg, $cupcakeLi);

   return $cupcakeDiv;
}

//function to show all of the cupcakes from the DB
async function showCupcakes() {
   const response = await axios.get(`${BASE_URL}`);
   for (let cupcake of response.data.cupcakes) {
      let newCupcake = $(addCupcakeHTML(cupcake));
      $cupcakesList.append(newCupcake);
   }
}

//event listener for the form submission to add the new cupcake to the DB and to the DOM
$cupcakeForm.on('submit', async function (e) {
   e.preventDefault();

   let flavor = $('#flavor').val();
   let size = $('#size').val();
   let rating = $('#rating').val();
   let image = $('#image').val();

   const newCupcakeResponse = await axios.post(`${BASE_URL}`, {
      flavor,
      size,
      rating,
      image,
   }); //in JS, if you want the key/val to be the same, you can just put one

   let cupcakeData = newCupcakeResponse.data.cupcake;
   let newCupcake = $(addCupcakeHTML(cupcakeData));

   $cupcakesList.append(newCupcake);
   $cupcakeForm.trigger('reset');
});

//event listener for the delete button to delete the cupcake from the DOM and DB
$cupcakesList.on('click', '.delete-cupcake', async function (e) {
   e.preventDefault();

   let $cupcake = $(e.target).closest('div'); //.closest traverses up the DOM tree to find the nearest parent element
   let cupcakeID = $cupcake.attr('data-id');

   const response = await axios.delete(`${BASE_URL}/${cupcakeID}`);

   $cupcake.remove();
});

showCupcakes();
