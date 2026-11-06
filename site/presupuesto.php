<?php
// Recibe el formulario de presupuesto de gebrey.es y lo manda por correo a hola@gebrey.es.
// Responde JSON si lo pide el JS de la página; si no (sin JS), redirige a gracias.html.
$json = str_contains($_SERVER['HTTP_ACCEPT'] ?? '', 'application/json');
$responder = function (bool $ok, string $error = '') use ($json) {
    if ($json) { header('Content-Type: application/json; charset=utf-8'); echo json_encode(['ok' => $ok, 'error' => $error]); }
    elseif ($ok) { header('Location: /gracias.html', true, 303); }
    else { header('Content-Type: text/plain; charset=utf-8'); if (http_response_code() === 200) http_response_code(400); echo $error; }
    exit;
};
if (($_SERVER['REQUEST_METHOD'] ?? '') !== 'POST') { http_response_code(405); $responder(false, 'Solo se admite POST.'); }
// cebo para robots: el campo "web" lo rellenan ellos, nunca una persona (va oculto); y nadie escribe en menos de 3 s
if (!empty($_POST['web'])) $responder(true);
$t = (int)($_POST['t'] ?? 0);
if ($t > 0 && time() - $t < 3) $responder(true);

$campo = function (string $k, int $max) {
    $v = trim(strip_tags((string)($_POST[$k] ?? '')));
    $v = preg_replace('/[\r\n\t\x00-\x1f]+/', ' ', $v);
    return mb_substr($v, 0, $max);
};
$tipo = $campo('tipo', 60); $para = $campo('para', 120); $que = $campo('que', 160); $cuando = $campo('cuando', 40);
$nombre = $campo('nombre', 80); $correo = filter_var($campo('correo', 120), FILTER_VALIDATE_EMAIL);
$mas = mb_substr(trim(strip_tags((string)($_POST['mas'] ?? ''))), 0, 3000);
if ($nombre === '' || !$correo) $responder(false, 'Falta tu nombre o un correo válido.');
if ($para === '' && $que === '' && $mas === '') $responder(false, 'Cuéntame al menos qué quieres.');

$frase = "Quiero $tipo para $para, que sobre todo tiene que $que. Lo necesito $cuando.\nMe llamo $nombre y me escribes a $correo.";
$cuerpo = $frase . ($mas !== '' ? "\n\n$mas" : '') . "\n\n— Enviado desde el formulario de gebrey.es el " . date('d/m/Y H:i') . " · IP " . ($_SERVER['REMOTE_ADDR'] ?? '?');
$asunto = '=?UTF-8?B?' . base64_encode("Presupuesto: $tipo para $para") . '?=';
$nombreCod = '=?UTF-8?B?' . base64_encode($nombre) . '?=';
$cabeceras = "From: GEBREY <hola@gebrey.es>\r\nReply-To: $nombreCod <$correo>\r\nContent-Type: text/plain; charset=UTF-8\r\nContent-Transfer-Encoding: 8bit\r\n";
$ok = @mail('hola@gebrey.es', $asunto, $cuerpo, $cabeceras);
$responder($ok, $ok ? '' : 'No se ha podido enviar. Escríbeme a hola@gebrey.es.');
