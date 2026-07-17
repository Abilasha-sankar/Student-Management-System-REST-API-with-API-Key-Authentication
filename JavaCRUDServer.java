import com.sun.net.httpserver.HttpServer;
import com.sun.net.httpserver.HttpExchange;
import java.io.OutputStream;
import java.net.InetSocketAddress;
import java.net.URLDecoder;
import java.nio.charset.StandardCharsets;
import java.util.HashMap;
public class JavaCRUDServer {
    static HashMap<Integer, String> students = new HashMap<>();
    static final String API_KEY = "STUDENT123";
    public static void main(String[] args) throws Exception {
        // CHANGED PORT → 8081 (NO CONFLICT)
        HttpServer server = HttpServer.create(new InetSocketAddress(8081), 0);
        server.createContext("/student", (HttpExchange exchange) -> {
            // CORS
            exchange.getResponseHeaders().add("Access-Control-Allow-Origin", "*");
            exchange.getResponseHeaders().add("Access-Control-Allow-Headers", "X-API-KEY");
            exchange.getResponseHeaders().add("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS");
            if (exchange.getRequestMethod().equalsIgnoreCase("OPTIONS")) {
                exchange.sendResponseHeaders(204, -1);
                exchange.close();
                return;
            }
            // API KEY CHECK
            String key = exchange.getRequestHeaders().getFirst("X-API-KEY");
            if (key == null || !key.equals(API_KEY)) {
                String response = "Invalid API Key";
                exchange.sendResponseHeaders(401, response.getBytes().length);
                OutputStream os = exchange.getResponseBody();
                os.write(response.getBytes());
                os.close();
                return;
            }
            String method = exchange.getRequestMethod();
            String query = exchange.getRequestURI().getQuery();
            int id = 0;
            String name = "";
            if (query != null) {
                String[] params = query.split("&");
                for (String p : params) {
                    String[] pair = p.split("=");
                    if (pair.length > 1) {
                        if (pair[0].equals("id")) {
                            id = Integer.parseInt(pair[1]);
                        }
                        if (pair[0].equals("name")) {
                            name = URLDecoder.decode(pair[1], StandardCharsets.UTF_8);
                        }
                    }
                }
            }
            String response;
            switch (method) {
                case "POST":
                    if (students.containsKey(id)) {
                        response = "Student already exists!";
                    } else {
                        students.put(id, name);
                        response = "Created Successfully\nID: " + id + "\nName: " + name;
                    }
                    break;
                case "GET":
                    if (students.isEmpty()) {
                        response = "No Students Found";
                    } else {
                        StringBuilder sb = new StringBuilder();
                        sb.append("==== STUDENT LIST ====\n");
                        for (Integer sid : students.keySet()) {
                            sb.append("ID: ").append(sid)
                              .append(" Name: ").append(students.get(sid))
                              .append("\n");
                        }
                        sb.append("Total: ").append(students.size());
                        response = sb.toString();
                    }
                    break;
                case "PUT":
                    if (students.containsKey(id)) {
                        students.put(id, name);
                        response = "Updated Successfully";
                    } else {
                        response = "Student Not Found";
                    }
                    break;
                case "DELETE":
                    if (students.containsKey(id)) {
                        students.remove(id);
                        response = "Deleted Successfully";
                    } else {
                        response = "Student Not Found";
                    }
                    break;
                default:
                    response = "Invalid Method";
            }
            System.out.println(response);
            exchange.sendResponseHeaders(200, response.getBytes().length);
            OutputStream os = exchange.getResponseBody();
            os.write(response.getBytes());
            os.close();
        });
        server.start();
        System.out.println("==================================");
        System.out.println(" CRUD SERVER STARTED (8081)");
        System.out.println(" API KEY: STUDENT123");
        System.out.println("==================================");
    }
}