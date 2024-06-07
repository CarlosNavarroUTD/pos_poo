class PuntoDeVenta {
    constructor() {
        this.inicializarEventos();
    }

    inicializarEventos() {
        $(document).ready(() => {
            $('#busqueda').autocomplete({
                source: (request, response) => {
                    $.ajax({
                        url: '/buscar_barcode',
                        data: {'term': request.term},
                        success: (data) => response(data),
                        error: (xhr, status, error) => console.error("Error en la solicitud AJAX:", error)
                    });
                },
                minLength: 2,
                select: (event, ui) => {
                    console.log("Seleccionado:", ui.item.label);
                    this.agregarFilaDesdeBarcode(ui.item.value);
                }
            });

            $('#btnProcesarVenta').on('click', () => this.procesarVenta());

            $(document).on('change', '.cantidad_unidades', () => this.actualizarTotalVenta());
        });
    }

    actualizarTotalVenta() {
        let totalVenta = 0;

        $('#tablaProductos tbody tr').each(function() {
            const precioPorUnidad = parseFloat($(this).find('td:nth-child(3)').text());
            const cantidadUnidades = parseInt($(this).find('td:nth-child(5) input').val());
            totalVenta += precioPorUnidad * cantidadUnidades;
        });

        $('#totalVenta').text('Total de la Venta: $' + totalVenta.toFixed(2));
    }

    agregarFilaTabla(data) {
        if (!Array.isArray(data)) {
            data = [data];
        }
        console.log(data);

        data.forEach(item => {
            const fila = $('<tr>');
            fila.append(`<td>${item.Barcode}</td>`);
            fila.append(`<td>${item.name_product}</td>`);
            fila.append(`<td>${item.precio_por_unidad}</td>`);
            fila.append(`<td>${item.precio_mayoreo}</td>`);
            fila.append('<td><input class="cantidad_unidades" type="number" value="1" min="1" step="1"></td>');

            $('#tablaProductos tbody').append(fila);
            this.actualizarTotalVenta();
        });
    }

    agregarFilaDesdeBarcode(barcode) {
        $.ajax({
            url: '/getall_frombarcode',
            data: {'selectedItem': barcode},
            type: 'GET',
            success: (data) => {
                this.agregarFilaTabla(data);
                $('#busqueda').val('');
            },
            error: (xhr, status, error) => console.error("Error en la segunda solicitud AJAX:", error)
        });
    }

    obtenerDatosTabla() {
        const totalVenta = [];

        $('#tablaProductos tbody tr').each(function() {
            const fila = $(this);
            const datosFila = {};

            fila.find('td').each(function(index) {
                const nombreColumna = $('#tablaProductos thead th:eq(' + index + ')').text().trim();
                const valorCelda = index === 4 ? $(this).find('input').val() : $(this).text().trim();
                datosFila[nombreColumna] = valorCelda;
            });

            totalVenta.push(datosFila);
        });

        return totalVenta;
    }

    procesarVenta() {
        if (confirm('¿Estás seguro que quieres terminar?')) {
            const datosTabla = this.obtenerDatosTabla();
            const datosJSON = JSON.stringify(datosTabla);
            console.log('Datos de la tabla:', datosJSON);

            $.ajax({
                url: '/registrar_venta',
                type: 'POST',
                contentType: 'application/json;charset=UTF-8',
                data: datosJSON,
                success: (response) => {
                    console.log('Respuesta JS-AJAX: "Venta procesada con éxito"');
                    console.log('Respuesta del servidor:', response);
                },
                error: (xhr, status, error) => console.error("Error en la solicitud AJAX:", error)
            });
        }
    }
}

$(document).ready(() => new PuntoDeVenta());
