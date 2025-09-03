import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.SQLException;
import java.sql.Statement;

public class Sample {
    public static void main(String[] args) throws ClassNotFoundException, SQLException {
        Class.forName("com.mysql.cj.jdbc.Driver");
        Connection conn = DriverManager.getConnection(
            "jdbc:mysql://localhost:3306/amity",
            "root",
            ""
        );
        Statement st = conn.createStatement();
        int i = st.executeUpdate("INSERT INTO s VALUES (1234, 'amit', 'BPHARMA')");
        System.out.println("No of rows affected = " + i);
        st.close();
        conn.close();
    }
}
