<!DOCTYPE html>
<html>
<head>
<title>Gestor SVG</title>
<link href="/GestorSvg/css/styleSheet.css" rel="stylesheet" />
<meta charset="utf-8">
</head>

<body>
	<header>
		<h1>Gestor Imágenes SVG en eXist</h1>
		<h3>SW 2023</h3>
	</header>

	<% if (request.getAttribute("informacion") != null) { %>
	<section>
		<font>Informacion:</font>
		<%=request.getAttribute("informacion")%>
	</section>
	<%	}%>

	<section>
		<form id="LeerRecursos" method="GET" action="/GestorSvg/apiLR">
			<table>
				<tr><td>Selecionar Colección:</td>
					<td><input id="collection" required name="collection" /></td>
				</tr>
			</table>
		</form>
		<hr/>
		<button type="submit" id="index" form="LeerRecursos">Ver Imagenes</button>
	</section>

	<section>
		<form id="ImagenNueva" method="GET" action="/GestorSvg/apiNI">
			<table>
				<tr><td>Nombre:</td>
					<td><input id="resource" required name="svgName" /></td>
				</tr>
				<tr><td>Colección:</td>
					<td><input id="collection" required name="collection" /></td>
				</tr>
			</table>
		</form>
		<hr/>
		<button id="index" form="ImagenNueva">Nueva Imagen</button>
	</section>

	<section>
		<form id="CrearColeccion" method="GET" action="/GestorSvg/apiCC">
			<table>
				<tr><td>Nombre Nueva Colección:</td>
					<td><input id="collection" required name="collection" /></td>
				</tr>
			</table>
		</form>
		<hr/>
		<button type="submit" id="index" form="CrearColeccion">Crear Coleccion</button>
	</section>

	<section>
		<form id="BorrarColeccion" method="GET" action="/GestorSvg/apiDC">
			<table>
				<tr><td>Selecionar Colección:</td>
					<td><input id="collection" required name="collection" /></td>
				</tr>
			</table>
		</form>
		<hr/>
		<button id="index" form="BorrarColeccion">Borrar Coleccion</button>
	</section>

	<footer>Sistemas Web - Escuela Ingeniería de Bilbao</footer>
</body>
</html>