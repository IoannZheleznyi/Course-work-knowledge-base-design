document.addEventListener("DOMContentLoaded", () => {
    const hero = document.getElementById("hero");
    const resultsPage = document.getElementById("resultsPage");

    const searchForm = document.getElementById("searchForm");
    const resultsSearchForm = document.getElementById("resultsSearchForm");

    const searchInput = document.getElementById("searchInput");
    const resultsSearchInput = document.getElementById("resultsSearchInput");

    const resultsContainer = document.getElementById("resultsContainer");
    const resultsTitle = document.getElementById("resultsTitle");
    const resultsSubtitle = document.getElementById("resultsSubtitle");
    const loading = document.getElementById("loading");

    searchForm.addEventListener("submit", event => {
        event.preventDefault();
        performSearch(searchInput.value);
    });

    resultsSearchForm.addEventListener("submit", event => {
        event.preventDefault();
        performSearch(resultsSearchInput.value);
    });

    document.getElementById("backButton").addEventListener("click", () => {
        resultsPage.classList.add("hidden");
        hero.classList.remove("hidden");
        searchInput.focus();
    });

    async function performSearch(query) {
        query = query.trim();

        if (!query) return;

        hero.classList.add("hidden");
        resultsPage.classList.remove("hidden");

        resultsSearchInput.value = query;
        resultsTitle.textContent = `Результаты поиска по запросу «${query}»`;
        resultsSubtitle.textContent = "Поиск по базе знаний и интернет-источникам";

        resultsContainer.innerHTML = "";
        loading.classList.remove("hidden");

        window.scrollTo({ top: 0, behavior: "smooth" });

        try {
            const response = await fetch(
                `/api/search?q=${encodeURIComponent(query)}`
            );

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.error || "Ошибка поиска");
            }

            loading.classList.add("hidden");
            renderResults(data);

        } catch (error) {
            loading.classList.add("hidden");

            resultsContainer.innerHTML = `
                <div class="status-message">
                    ${escapeHTML(error.message)}
                </div>
            `;

            console.error(error);
        }
    }

    function renderResults(data) {
        const knowledge = data.knowledge_base || [];
        const internet = data.internet || {};

        let html = "";

        if (knowledge.length > 0) {
            html += `
                <section class="result-section">
                    <div class="section-heading">
                        <span class="section-symbol">✦</span>
                        <div>
                            <h2>Информация из базы знаний</h2>
                            <p>Материалы собственной базы SpiceSearch</p>
                        </div>
                    </div>

                    <div class="knowledge-grid">
                        ${knowledge.map(renderKnowledge).join("")}
                    </div>
                </section>
            `;
        }

        if (knowledge.length === 0 && internet.description) {
            html += `
                <section class="result-section">
                    <div class="section-heading">
                        <span class="section-symbol">ℹ</span>
                        <div>
                            <h2>Описание из интернета</h2>
                            <p>Дополнительная информация о специи</p>
                        </div>
                    </div>

                    <article class="internet-description">
                        <h3>${escapeHTML(internet.description.title)}</h3>
                        <p>${escapeHTML(internet.description.text)}</p>
                        <a href="${safeURL(internet.description.url)}"
                           target="_blank" rel="noopener noreferrer">
                            Читать полный материал →
                        </a>
                        <span class="description-source">
                            Источник: ${escapeHTML(internet.description.source_name)}
                        </span>
                    </article>
                </section>
            `;
        }

        if (internet.images && internet.images.length > 0) {
            html += `
                <section class="result-section">
                    <div class="section-heading">
                        <span class="section-symbol">▧</span>
                        <div>
                            <h2>Изображения</h2>
                            <p>Фотографии из Wikimedia Commons</p>
                        </div>
                    </div>

                    <div class="image-grid">
                        ${internet.images.map(renderImage).join("")}
                    </div>
                </section>
            `;
        }

        if (internet.videos && internet.videos.length > 0) {
            html += `
                <section class="result-section">
                    <div class="section-heading">
                        <span class="section-symbol">▶</span>
                        <div>
                            <h2>Видео</h2>
                            <p>Видеоматериалы с YouTube</p>
                        </div>
                    </div>

                    <div class="video-grid">
                        ${internet.videos.map(renderVideo).join("")}
                    </div>
                </section>
            `;
        }

        if (internet.news && internet.news.length > 0) {
            html += `
                <section class="result-section">
                    <div class="section-heading">
                        <span class="section-symbol">▤</span>
                        <div>
                            <h2>Статьи и новости</h2>
                            <p>Публикации из интернет-источников</p>
                        </div>
                    </div>

                    <div class="news-list">
                        ${internet.news.map(renderNews).join("")}
                    </div>
                </section>
            `;
        }

        const hasResults =
            knowledge.length > 0 ||
            Boolean(internet.description) ||
            (internet.images || []).length > 0 ||
            (internet.videos || []).length > 0 ||
            (internet.news || []).length > 0;

        if (!hasResults) {
            html += `
                <div class="status-message">
                    По вашему запросу ничего не найдено.
                    Попробуйте ввести название специи.
                </div>
            `;
        }

        if (!internet.youtube_configured && hasResults) {
            html += `
                <p class="integration-note">
                    Поиск видео появится после подключения YouTube API.
                </p>
            `;
        }

        resultsContainer.innerHTML = html;
    }

    function renderKnowledge(spice) {
        return `
            <article class="knowledge-card">
                <div class="knowledge-category">
                    ${escapeHTML(spice.category || "Специя")}
                </div>

                <h3>${escapeHTML(spice.name)}</h3>

                <p>${escapeHTML(spice.description || "")}</p>

                <div class="knowledge-details">
                    <div>
                        <strong>Происхождение</strong>
                        <span>${escapeHTML(spice.origin || "Не указано")}</span>
                    </div>

                    <div>
                        <strong>Применение</strong>
                        <span>${escapeHTML(spice.usage || "Не указано")}</span>
                    </div>
                </div>

                ${renderDatabaseMaterials(spice)}
            </article>
        `;
    }

    function renderDatabaseMaterials(spice) {
        const articles = spice.articles || [];

        if (!articles.length) return "";

        return `
            <div class="database-materials">
                <h4>Дополнительные материалы базы</h4>

                ${articles.map(article => `
                    <div class="database-article">
                        <strong>${escapeHTML(article.title)}</strong>
                        <p>${escapeHTML(article.description || "")}</p>

                        ${article.source_url ? `
                            <a href="${safeURL(article.source_url)}"
                               target="_blank" rel="noopener noreferrer">
                                Открыть источник →
                            </a>
                        ` : ""}
                    </div>
                `).join("")}
            </div>
        `;
    }

    function renderImage(item) {
        return `
            <a class="image-card"
               href="${safeURL(item.source_url)}"
               target="_blank" rel="noopener noreferrer">

                <img src="${safeURL(item.image_url)}"
                     alt="${escapeHTML(item.title)}"
                     loading="lazy">

                <span>${escapeHTML(item.title)}</span>
            </a>
        `;
    }

    function renderVideo(item) {
        return `
            <a class="video-card"
               href="${safeURL(item.video_url)}"
               target="_blank" rel="noopener noreferrer">

                <div class="video-thumbnail">
                    ${item.thumbnail ? `
                        <img src="${safeURL(item.thumbnail)}"
                             alt="${escapeHTML(item.title)}"
                             loading="lazy">
                    ` : ""}

                    <span class="play-icon">▶</span>
                </div>

                <div class="video-info">
                    <h3>${escapeHTML(item.title)}</h3>
                    <p>${escapeHTML(item.source_name || "YouTube")}</p>
                </div>
            </a>
        `;
    }

    function renderNews(item) {
        return `
            <article class="news-card">
                <h3>
                    <a href="${safeURL(item.url)}"
                       target="_blank" rel="noopener noreferrer">
                        ${escapeHTML(item.title)}
                    </a>
                </h3>

                <div class="news-meta">
                    <span>${escapeHTML(item.source_name || "Источник")}</span>
                    <span>${escapeHTML(item.published_at || "")}</span>
                </div>
            </article>
        `;
    }

    function safeURL(value) {
        try {
            const url = new URL(value, window.location.origin);

            if (url.protocol === "https:" || url.protocol === "http:") {
                return url.href;
            }
        } catch (error) {
            console.error("Некорректная ссылка", error);
        }

        return "#";
    }

    function escapeHTML(value) {
        return String(value).replace(/[&<>"']/g, character => ({
            "&": "&amp;",
            "<": "&lt;",
            ">": "&gt;",
            '"': "&quot;",
            "'": "&#039;"
        })[character]);
    }
});
