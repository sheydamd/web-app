const API_URL = "http://127.0.0.1:8000";

let currentPage = 1;
const limit = 10;


async function loadGarages() {

    const search = document
        .getElementById("searchInput")
        .value;

    const city = document
        .getElementById("citySelect")
        .value;


    const params = new URLSearchParams();

    params.append("page", currentPage);
    params.append("limit", limit);

    if (search) {
        params.append("name", search);
    }

    if (city) {
        params.append("city", city);
    }


    try {

        const response = await fetch(
            `${API_URL}/api/garages/?${params.toString()}`
        );

        if (!response.ok) {
            throw new Error("Failed to load garages");
        }

        const garages = await response.json();

        displayGarages(garages);

    } catch (error) {

        console.error(error);

        document.getElementById(
            "garageList"
        ).innerHTML = `
            <p>
                دریافت اطلاعات با خطا مواجه شد.
            </p>
        `;
    }
}


function displayGarages(garages) {

    const garageList =
        document.getElementById("garageList");

    const resultCount =
        document.getElementById("resultCount");


    resultCount.textContent =
        `${garages.length} تعمیرگاه`;


    if (garages.length === 0) {

        garageList.innerHTML = `
            <p>
                تعمیرگاهی پیدا نشد.
            </p>
        `;

        return;
    }


    garageList.innerHTML = "";


    garages.forEach(garage => {

        const card =
            document.createElement("div");

        card.className = "garage-card";


        card.innerHTML = `
            <h3>${garage.name}</h3>

            <p>
                📍 ${garage.address}
            </p>

            <p>
                📞 ${garage.phone || "ثبت نشده"}
            </p>

            <p>
                شهر: ${garage.city || "ثبت نشده"}
            </p>

            <p class="rating">
                ⭐ ${garage.rating || 0}
                (${garage.review_count || 0} نظر)
            </p>

            <button
                class="details-button"
                onclick="showGarage(${garage.id})"
            >
                مشاهده جزئیات
            </button>
        `;


        garageList.appendChild(card);
    });
}


function searchGarages() {

    currentPage = 1;

    loadGarages();
}


function nextPage() {

    currentPage++;

    loadGarages();
}


function previousPage() {

    if (currentPage <= 1) {
        return;
    }

    currentPage--;

    loadGarages();
}


async function showGarage(garageId) {

    try {

        const response = await fetch(
            `${API_URL}/api/garages/${garageId}`
        );

        if (!response.ok) {
            throw new Error("Garage not found");
        }

        const garage = await response.json();

        alert(
            `نام: ${garage.name}\n` +
            `آدرس: ${garage.address}\n` +
            `تلفن: ${garage.phone || "ثبت نشده"}\n` +
            `امتیاز: ${garage.rating || 0}`
        );

    } catch (error) {

        alert(
            "دریافت اطلاعات تعمیرگاه با خطا مواجه شد."
        );
    }
}


loadGarages();