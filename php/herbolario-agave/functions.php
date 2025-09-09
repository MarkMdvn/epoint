// Mark Mordvin - Gestión de Negocios Digitales S.L | 18/06/2025

// mark.mordvin@epoint.es - Edición del formulario "checkout" para la funcionalidad de las facturas

add_action( 'woocommerce_after_checkout_billing_form', 'mm_add_checkout_invoice_fields' );
function mm_add_checkout_invoice_fields( $checkout ) {
    $provinces = array(
        ''              => __( 'Selecciona una provincia...', 'woocommerce' ),
        'Álava'         => __( 'Álava', 'woocommerce' ),
        'Albacete'      => __( 'Albacete', 'woocommerce' ),
        'Alicante'      => __( 'Alicante', 'woocommerce' ),
        'Almería'       => __( 'Almería', 'woocommerce' ),
        'Asturias'      => __( 'Asturias', 'woocommerce' ),
        'Ávila'         => __( 'Ávila', 'woocommerce' ),
        'Badajoz'       => __( 'Badajoz', 'woocommerce' ),
        'Baleares'      => __( 'Baleares', 'woocommerce' ),
        'Barcelona'     => __( 'Barcelona', 'woocommerce' ),
        'Burgos'        => __( 'Burgos', 'woocommerce' ),
        'Cáceres'       => __( 'Cáceres', 'woocommerce' ),
        'Cádiz'         => __( 'Cádiz', 'woocommerce' ),
        'Cantabria'     => __( 'Cantabria', 'woocommerce' ),
        'Castellón'     => __( 'Castellón', 'woocommerce' ),
        'Ceuta'         => __( 'Ceuta', 'woocommerce' ),
        'Ciudad Real'   => __( 'Ciudad Real', 'woocommerce' ),
        'Córdoba'       => __( 'Córdoba', 'woocommerce' ),
        'La Coruña'     => __( 'La Coruña', 'woocommerce' ),
        'Cuenca'        => __( 'Cuenca', 'woocommerce' ),
        'Gerona'        => __( 'Gerona', 'woocommerce' ),
        'Granada'       => __( 'Granada', 'woocommerce' ),
        'Guadalajara'   => __( 'Guadalajara', 'woocommerce' ),
        'Guipúzcoa'     => __( 'Guipúzcoa', 'woocommerce' ),
        'Huelva'        => __( 'Huelva', 'woocommerce' ),
        'Huesca'        => __( 'Huesca', 'woocommerce' ),
        'Jaén'          => __( 'Jaén', 'woocommerce' ),
        'León'          => __( 'León', 'woocommerce' ),
        'Lérida'        => __( 'Lérida', 'woocommerce' ),
        'Lugo'          => __( 'Lugo', 'woocommerce' ),
        'Madrid'        => __( 'Madrid', 'woocommerce' ),
        'Málaga'        => __( 'Málaga', 'woocommerce' ),
        'Melilla'       => __( 'Melilla', 'woocommerce' ),
        'Murcia'        => __( 'Murcia', 'woocommerce' ),
        'Navarra'       => __( 'Navarra', 'woocommerce' ),
        'Orense'        => __( 'Orense', 'woocommerce' ),
        'Palencia'      => __( 'Palencia', 'woocommerce' ),
        'Las Palmas'    => __( 'Las Palmas', 'woocommerce' ),
        'Pontevedra'    => __( 'Pontevedra', 'woocommerce' ),
        'La Rioja'      => __( 'La Rioja', 'woocommerce' ),
        'Salamanca'     => __( 'Salamanca', 'woocommerce' ),
        'Segovia'       => __( 'Segovia', 'woocommerce' ),
        'Sevilla'       => __( 'Sevilla', 'woocommerce' ),
        'Soria'         => __( 'Soria', 'woocommerce' ),
        'Tarragona'     => __( 'Tarragona', 'woocommerce' ),
        'Santa Cruz de Tenerife' => __( 'Santa Cruz de Tenerife', 'woocommerce' ),
        'Teruel'        => __( 'Teruel', 'woocommerce' ),
        'Toledo'        => __( 'Toledo', 'woocommerce' ),
        'Valencia'      => __( 'Valencia', 'woocommerce' ),
        'Valladolid'    => __( 'Valladolid', 'woocommerce' ),
        'Vizcaya'       => __( 'Vizcaya', 'woocommerce' ),
        'Zamora'        => __( 'Zamora', 'woocommerce' ),
        'Zaragoza'      => __( 'Zaragoza', 'woocommerce' ),
    );

    echo '<div id="mm_invoice_fields_container" style="clear:both;">';
    echo '<h3>' . __('¿Necesitas factura?', 'woocommerce') . '</h3>';

    woocommerce_form_field( 'mm_needs_invoice', array(
        'type'          => 'checkbox',
        'class'         => array('form-row-wide'),
        'label'         => __('Sí, quiero factura', 'woocommerce'),
        'required'      => false,
    ), $checkout->get_value( 'mm_needs_invoice' ));

    echo '<div class="mm-invoice-dependent-fields" style="display:none;">';

    woocommerce_form_field( 'mm_invoice_name', array(
        'type'          => 'text',
        'class'         => array('form-row-wide'),
        'label'         => __('Nombre o Razón Social', 'woocommerce'),
        'placeholder'   => __('Escribe el nombre completo para la factura', 'woocommerce'),
        'required'      => true,
    ), $checkout->get_value( 'mm_invoice_name' ));

    woocommerce_form_field( 'mm_invoice_vat', array(
        'type'          => 'text',
        'class'         => array('form-row-wide'),
        'label'         => __('NIF / CIF', 'woocommerce'),
        'placeholder'   => __('Introduce tu número de identificación fiscal', 'woocommerce'),
        'required'      => true,
    ), $checkout->get_value( 'mm_invoice_vat' ));

    woocommerce_form_field( 'mm_invoice_street', array(
        'type'          => 'text',
        'class'         => array('form-row-wide'),
        'label'         => __('Calle y Número', 'woocommerce'),
        'placeholder'   => __('Ej: Calle Mayor, 123', 'woocommerce'),
        'required'      => true,
    ), $checkout->get_value( 'mm_invoice_street' ));

    woocommerce_form_field( 'mm_invoice_city', array(
        'type'          => 'text',
        'class'         => array('form-row-wide'),
        'label'         => __('Población', 'woocommerce'),
        'placeholder'   => __('Ej: Madrid', 'woocommerce'),
        'required'      => true,
    ), $checkout->get_value( 'mm_invoice_city' ));

    woocommerce_form_field( 'mm_invoice_postcode', array(
        'type'          => 'text',
        'class'         => array('form-row-wide'),
        'label'         => __('Código Postal', 'woocommerce'),
        'placeholder'   => __('Ej: 28001', 'woocommerce'),
        'required'      => true,
    ), $checkout->get_value( 'mm_invoice_postcode' ));

    woocommerce_form_field( 'mm_invoice_state', array(
        'type'          => 'select',
        'class'         => array('form-row-wide'),
        'label'         => __('Provincia', 'woocommerce'),
        'required'      => true,
        'options'       => $provinces,
    ), $checkout->get_value( 'mm_invoice_state' ));

    echo '</div></div>';
}

add_action( 'wp_footer', 'mm_invoice_fields_script' );
function mm_invoice_fields_script() {
    if ( ! is_checkout() ) {
        return;
    }
    ?>
    <script type="text/javascript">
        jQuery(document).ready(function($){
            function toggleInvoiceFields() {
                if ($('input#mm_needs_invoice').is(':checked')) {
                    $('.mm-invoice-dependent-fields').slideDown();
                } else {
                    $('.mm-invoice-dependent-fields').slideUp();
                }
            }

            function initSearchableDropdown() {
                if ($.fn.select2) {
                    $('select#mm_invoice_state').select2();
                }
            }

            toggleInvoiceFields();
            initSearchableDropdown();

            $(document.body).on('updated_checkout', function(){
                toggleInvoiceFields();
                initSearchableDropdown();
            });

            $('body').on('change', 'input#mm_needs_invoice', function(){
                toggleInvoiceFields();
            });
        });
    </script>
    <?php
}

add_action('woocommerce_checkout_process', 'mm_validate_invoice_fields');
function mm_validate_invoice_fields() {
    if ( isset($_POST['mm_needs_invoice']) && $_POST['mm_needs_invoice'] == 1 ) {

        if ( empty($_POST['mm_invoice_name']) ) {
            wc_add_notice( __( 'Por favor, introduce un nombre o razón social para la factura.' ), 'error' );
        }

        if ( empty($_POST['mm_invoice_vat']) ) {
            wc_add_notice( __( 'Por favor, introduce tu NIF / CIF para la factura.' ), 'error' );
        }

        if ( empty($_POST['mm_invoice_street']) ) {
            wc_add_notice( __( 'Por favor, introduce la calle para la factura.' ), 'error' );
        }
        if ( empty($_POST['mm_invoice_city']) ) {
            wc_add_notice( __( 'Por favor, introduce la población para la factura.' ), 'error' );
        }
        if ( empty($_POST['mm_invoice_postcode']) ) {
            wc_add_notice( __( 'Por favor, introduce el código postal para la factura.' ), 'error' );
        }
        if ( empty($_POST['mm_invoice_state']) ) {
            wc_add_notice( __( 'Por favor, selecciona una provincia para la factura.' ), 'error' );
        }
    }
}

add_action( 'woocommerce_checkout_create_order', 'mm_save_invoice_fields_to_order_meta', 10, 2 );
function mm_save_invoice_fields_to_order_meta( $order, $data ) {
    if ( isset( $_POST['mm_needs_invoice'] ) && $_POST['mm_needs_invoice'] == 1 ) {
        $order->update_meta_data( '_mm_needs_invoice', 'yes' );

        if ( ! empty( $_POST['mm_invoice_name'] ) ) {
            $order->update_meta_data( '_mm_invoice_name', sanitize_text_field( $_POST['mm_invoice_name'] ) );
        }
        if ( ! empty( $_POST['mm_invoice_vat'] ) ) {
            $order->update_meta_data( '_mm_invoice_vat', sanitize_text_field( $_POST['mm_invoice_vat'] ) );
        }

        if ( ! empty( $_POST['mm_invoice_street'] ) ) {
            $order->update_meta_data( '_mm_invoice_street', sanitize_text_field( $_POST['mm_invoice_street'] ) );
        }
        if ( ! empty( $_POST['mm_invoice_city'] ) ) {
            $order->update_meta_data( '_mm_invoice_city', sanitize_text_field( $_POST['mm_invoice_city'] ) );
        }
        if ( ! empty( $_POST['mm_invoice_postcode'] ) ) {
            $order->update_meta_data( '_mm_invoice_postcode', sanitize_text_field( $_POST['mm_invoice_postcode'] ) );
        }
        if ( ! empty( $_POST['mm_invoice_state'] ) ) {
            $order->update_meta_data( '_mm_invoice_state', sanitize_text_field( $_POST['mm_invoice_state'] ) );
        }

    } else {
        $order->update_meta_data( '_mm_needs_invoice', 'no' );
    }
}

// mark.mordvin@epoint.es - Numeración personalizada en las facturas


add_action( 'woocommerce_order_status_completed', 'mm_generate_and_inject_invoice_on_completion', 999, 1 );
function mm_generate_and_inject_invoice_on_completion( $order_id ) {
    $order = wc_get_order( $order_id );
    if ( ! $order ) {
        return;
    }

    if ( $order->get_meta( '_mm_needs_invoice' ) !== 'yes' ) {
        return;
    }

    $counter_option_name = 'mm_herbolario_invoice_counter';
    $number_to_assign    = (int) get_option( $counter_option_name, 0 );

    $invoice_settings = get_option( 'wpo_wcpdf_documents_settings_invoice', array() );
    $prefix           = isset( $invoice_settings['number_format']['prefix'] ) ? $invoice_settings['number_format']['prefix'] : '';
    $suffix           = isset( $invoice_settings['number_format']['suffix'] ) ? $invoice_settings['number_format']['suffix'] : '';
    $padding          = isset( $invoice_settings['number_format']['padding'] ) ? $invoice_settings['number_format']['padding'] : '';

    $padded_number = $number_to_assign;
    if ( ! empty( $padding ) && is_numeric( $padding ) ) {
        $padded_number = sprintf( '%0' . $padding . 'd', $number_to_assign );
    }

    $formatted_number = "{$prefix}{$padded_number}{$suffix}";

    delete_post_meta( $order_id, '_wcpdf_invoice_number' );
    delete_post_meta( $order_id, '_wcpdf_invoice_number_data' );

    $invoice_number_data = array(
        'number'           => $number_to_assign,
        'formatted_number' => $formatted_number,
        'prefix'           => $prefix,
        'suffix'           => $suffix,
        'document_type'    => 'invoice',
        'order_id'         => $order_id,
        'padding'          => $padding,
    );

    $invoice_number = $formatted_number;

    add_post_meta( $order_id, '_wcpdf_invoice_number', $invoice_number, true );
    add_post_meta( $order_id, '_wcpdf_invoice_number_data', $invoice_number_data, true );
    add_post_meta( $order_id, '_wcpdf_invoice_date', time(), true );
    add_post_meta( $order_id, '_wcpdf_invoice_date_formatted', date_i18n( wc_date_format(), time() ), true );

    $next_number = $number_to_assign + 1;
    update_option( $counter_option_name, $next_number );

    $order->add_order_note( "Custom invoice #{$formatted_number} generated (sequential numbering)." );
}

add_action( 'woocommerce_order_status_completed', 'mm_force_custom_invoice_number', 9999, 1 );
function mm_force_custom_invoice_number( $order_id ) {
    $order = wc_get_order( $order_id );
    if ( ! $order ) {
        return;
    }

    if ( $order->get_meta( '_mm_needs_invoice' ) !== 'yes' ) {
        return;
    }

    $counter_option_name = 'mm_herbolario_invoice_counter';
    $expected_number = (int) get_option( $counter_option_name, 0 ) - 1;

    $current_invoice_data = get_post_meta( $order_id, '_wcpdf_invoice_number_data', true );

    if ( is_array( $current_invoice_data ) && isset( $current_invoice_data['number'] ) ) {
        $current_number = (int) $current_invoice_data['number'];

        if ( $current_number !== $expected_number ) {
            $invoice_settings = get_option( 'wpo_wcpdf_documents_settings_invoice', array() );
            $prefix = isset( $invoice_settings['number_format']['prefix'] ) ? $invoice_settings['number_format']['prefix'] : '';
            $suffix = isset( $invoice_settings['number_format']['suffix'] ) ? $invoice_settings['number_format']['suffix'] : '';
            $padding = isset( $invoice_settings['number_format']['padding'] ) ? $invoice_settings['number_format']['padding'] : '';

            $padded_number = $expected_number;
            if ( ! empty( $padding ) && is_numeric( $padding ) ) {
                $padded_number = sprintf( '%0' . $padding . 'd', $expected_number );
            }

            $formatted_number = "{$prefix}{$padded_number}{$suffix}";

            $corrected_invoice_data = array(
                'number'           => $expected_number,
                'formatted_number' => $formatted_number,
                'prefix'           => $prefix,
                'suffix'           => $suffix,
                'document_type'    => 'invoice',
                'order_id'         => $order_id,
                'padding'          => $padding,
            );

            update_post_meta( $order_id, '_wcpdf_invoice_number', $formatted_number );
            update_post_meta( $order_id, '_wcpdf_invoice_number_data', $corrected_invoice_data );

            $order->add_order_note( "Invoice number corrected to sequential #{$formatted_number} (was #{$current_number})." );
        }
    }
}

/**
 * Mark Mordvin - Gestión de Negocios Digitales S.L | 09/09/2025
 * Previene la CREACIÓN de la factura si el cliente no la solicitó.
 * Este filtro actúa como un interruptor maestro para la generación de documentos del plugin.
 */
add_filter( 'wpo_wcpdf_document_is_allowed', 'mm_prevent_invoice_generation', 10, 2 );
function mm_prevent_invoice_generation( $allowed, $document ) {
    if ( ! $document || ! is_a( $document->order, 'WC_Order' ) ) {
        return $allowed;
    }

    if ( 'invoice' === $document->get_type() ) {
        $needs_invoice = $document->order->get_meta( '_mm_needs_invoice' );

        if ( $needs_invoice !== 'yes' ) {
            return false;
        }
    }


    return $allowed;
}

add_action( 'woocommerce_order_status_completed', 'mm_cleanup_unwanted_invoices', 50, 1 );
function mm_cleanup_unwanted_invoices( $order_id ) {
    $order = wc_get_order( $order_id );

    if ( ! $order ) {
        return;
    }

    $needs_invoice = $order->get_meta( '_mm_needs_invoice' );

    if ( $needs_invoice !== 'yes' ) {
        delete_post_meta( $order_id, '_wcpdf_invoice_number' );
        delete_post_meta( $order_id, '_wcpdf_formatted_invoice_number' );
        delete_post_meta( $order_id, '_wcpdf_invoice_date' );
        delete_post_meta( $order_id, '_wcpdf_invoice_number_data' );
        delete_post_meta( $order_id, '_wcpdf_invoice_date_formatted' );

        $order->add_order_note( 'Invoice generation prevented - customer opted out.' );
    }
}

// update_option( 'mm_herbolario_invoice_counter', -1 );

// Mark Mordvin - Gestión de Negocios Digitales S.L | 18/06/2025 - END


