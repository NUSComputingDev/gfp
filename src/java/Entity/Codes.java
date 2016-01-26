/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package Entity;

import java.io.Serializable;
import javax.persistence.Entity;
import javax.persistence.GeneratedValue;
import javax.persistence.GenerationType;
import javax.persistence.Id;

/**
 *
 * @author JmTiong
 */
@Entity
public class Codes implements Serializable {
  private static final long serialVersionUID = 1L;
  @Id
  @GeneratedValue(strategy = GenerationType.AUTO)
  private Long id;
  private String type;
  private String keyCode;
  private int isRedeemed;
  private double pointsWorth;

  public Long getId() {
    return id;
  }

  public void setId(Long id) {
    this.id = id;
  }

  @Override
  public int hashCode() {
    int hash = 0;
    hash += (getId() != null ? getId().hashCode() : 0);
    return hash;
  }

  @Override
  public boolean equals(Object object) {
    // TODO: Warning - this method won't work in the case the id fields are not set
    if (!(object instanceof Codes)) {
      return false;
    }
    Codes other = (Codes) object;
    if ((this.getId() == null && other.getId() != null) || (this.getId() != null && !this.id.equals(other.id))) {
      return false;
    }
    return true;
  }

  @Override
  public String toString() {
    return "entity.Codes[ id=" + getId() + " ]";
  }

  /**
   * @return the type
   */
  public String getType() {
    return type;
  }

  /**
   * @param type the type to set
   */
  public void setType(String type) {
    this.type = type;
  }

  /**
   * @return the key
   */
  public String getKeyCode() {
    return keyCode;
  }

  /**
   * @param key the key to set
   */
  public void setKeyCode(String key) {
    this.keyCode = key;
  }

  /**
   * @return the isRedeemed
   */
  public int getIsRedeemed() {
    return isRedeemed;
  }

  /**
   * @param isRedeemed the isRedeemed to set
   */
  public void setIsRedeemed(int isRedeemed) {
    this.isRedeemed = isRedeemed;
  }

  /**
   * @return the pointsWorth
   */
  public double getPointsWorth() {
    return pointsWorth;
  }

  /**
   * @param pointsWorth the pointsWorth to set
   */
  public void setPointsWorth(double pointsWorth) {
    this.pointsWorth = pointsWorth;
  }
  
}
