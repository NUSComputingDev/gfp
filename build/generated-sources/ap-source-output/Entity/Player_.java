package Entity;

import javax.annotation.Generated;
import javax.persistence.metamodel.SingularAttribute;
import javax.persistence.metamodel.StaticMetamodel;

@Generated(value="EclipseLink-2.5.2.v20140319-rNA", date="2016-01-26T16:48:10")
@StaticMetamodel(Player.class)
public class Player_ { 

    public static volatile SingularAttribute<Player, String> password;
    public static volatile SingularAttribute<Player, String> salt;
    public static volatile SingularAttribute<Player, String> qrcode;
    public static volatile SingularAttribute<Player, String> name;
    public static volatile SingularAttribute<Player, Long> id;
    public static volatile SingularAttribute<Player, String> type;
    public static volatile SingularAttribute<Player, String> email;
    public static volatile SingularAttribute<Player, Double> points;

}