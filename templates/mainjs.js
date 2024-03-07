<script>
    // Функция для прокрутки страницы до второго вірша при загрузке страницы
    window.onload = function() {
        // Проверяем, если id равен 2, то прокручиваем страницу до второго вірша
        var verseId = {{ verse.id }};
        if (verseId === 2) {
            var element = document.getElementById('verse-2');
            if (element) {
                element.scrollIntoView();
            }
        }
    };
</script>
