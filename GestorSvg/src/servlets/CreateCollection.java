package servlets;

import java.io.IOException;
import java.io.StringReader;
import java.net.HttpURLConnection;
import java.util.HashMap;
import java.util.Map;

import javax.servlet.RequestDispatcher;
import javax.servlet.ServletConfig;
import javax.servlet.ServletException;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import javax.xml.parsers.DocumentBuilder;
import javax.xml.parsers.DocumentBuilderFactory;

import org.w3c.dom.Document;
import org.w3c.dom.NodeList;
import org.xml.sax.InputSource;

import HTTPeXist.HTTPeXist;

public class CreateCollection extends HttpServlet {
	private static final long serialVersionUID = 1L;
	private HTTPeXist eXist;

	
	public void init(ServletConfig config) {
		System.out.println("---> Entrando en init()de CreateCollection");
		eXist = new HTTPeXist("http://localHost:8080");
		System.out.println("---> Saliendo de init()de CreateCollection");
	}
	
	
	protected void doGet(HttpServletRequest request, HttpServletResponse response)
			throws ServletException, IOException {
		String collection = "";
        collection = request.getParameter("collection");
        int status = eXist.create(collection);
        if (status == HttpURLConnection.HTTP_CREATED) {
            request.setAttribute("informacion", "Colección creada correctamente");
        } else {
            request.setAttribute("informacion", "Error al crear la colección");
        }
        request.getRequestDispatcher("/jsp/index.jsp").forward(request, response);

		}

	protected void doPost(HttpServletRequest request, HttpServletResponse response)
			throws ServletException, IOException {
		doGet(request, response);
	}
}
