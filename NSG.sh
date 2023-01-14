#!/bin/bash 
menu='Choose from options above:'
ch=("Create-NSG" "AddRules-NSG" "Quit")
select fav in "${ch[@]}"; do
  case $fav in 
     "Create-NSG")
     read -p 'Enter the compartment OCID:' cmpvar
     read -p 'Enter the VCN OCID:' vcnvar
     read -p 'Enter the NSG Name:' namvar
     oci network nsg create --compartment-id $cmpvar --vcn-id $vcnvar --display-name $namvar
    ;;
    "AddRules-NSG")
    read -p 'Enter the NSG OCID:' ocidvar
find NSG_Split*|while read nsgrulesfile;
 do oci network nsg rules add --nsg-id $ocidvar --security-rules file://$nsgrulesfile
done 
    ;;
    "Quit")
    echo "User requested exit"
    exit
    ;;
    *) echo "invalid option $REPLY";;
    esac
done