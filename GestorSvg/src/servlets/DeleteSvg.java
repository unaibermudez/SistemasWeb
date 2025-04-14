package servlets;

import java.io.IOException;
import java.net.HttpURLConnection;
import java.net.URL;

import javax.servlet.ServletException;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

import HTTPeXist.HTTPeXist;

public class DeleteSvg extends HttpServlet {
    private static final long serialVersionUID = 1L;
    private HTTPeXist eXist;

    public void init() {
        System.out.println("---> Entrando en init() de DeleteResource");
        eXist = new HTTPeXist("http://localhost:8080");
        System.out.println("---> Saliendo de init() de DeleteResource");
    }

    protected void doGet(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {
        String collection = request.getParameter("collection");
        String resourceName = request.getParameter("svgName");
        int status = eXist.delete(collection, resourceName);
        if (status == HttpURLConnection.HTTP_OK) {
            request.setAttribute("informacion", "Recurso eliminado exitosamente.");
        } else {
            request.setAttribute("informacion", "No se pudo eliminar el recurso.");
        }
        request.getRequestDispatcher("/jsp/index.jsp").forward(request, response);
    }

    protected void doPost(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {
        doGet(request, response);
    }
}
