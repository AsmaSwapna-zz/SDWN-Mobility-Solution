#!/usr/bin/python

"""
Setting the position of Nodes (only for Stations and Access Points) and providing mobility.

"""

from mininet.net import Mininet
from mininet.node import Controller,OVSKernelSwitch
from mininet.link import TCLink
from mininet.cli import CLI
from mininet.log import setLogLevel

def topology():

    "Create a network."
    net = Mininet( controller=Controller, link=TCLink, switch=OVSKernelSwitch )

    print "*** Creating nodes"
    h1 = net.addHost( 'h1', mac='00:00:00:00:00:01', ip='10.0.0.1/8' )
    sta1 = net.addStation( 'sta1', mac='00:00:00:00:00:02', ip='10.0.0.2/8' )
    sta2 = net.addStation( 'sta2', wlans=2, ip='10.0.0.3/8' )
    sta3 = net.addStation( 'sta3', mac='00:00:00:00:00:04', ip='10.0.0.4/8' )
    sta4 = net.addStation( 'sta4', wlans=2, ip='10.0.0.5/8' )
    sta5 = net.addStation( 'sta5', mac='00:00:00:00:00:06', ip='10.0.0.6/8' )
    sta6 = net.addStation( 'sta6', wlans=2,ip='10.0.0.7/8' )

    ap1 = net.addBaseStation( 'ap1', ssid= 'new-ssid1', mode= 'g', channel= '1', position='30,30,0', range= 30)
    ap2 = net.addBaseStation( 'ap2', ssid= 'new-ssid2', mode= 'g', channel= '2', position='60,30,0', range= 40 )
    ap3 = net.addBaseStation( 'ap3', ssid= 'new-ssid3', mode= 'g', channel= '3', position='30,50,0', range= 35 )
    ap4 = net.addBaseStation( 'ap4', ssid= 'new-ssid4', mode= 'g', channel= '4', position='60,50,0', range= 45 )
    c1 = net.addController( 'c1', controller=Controller )


    print "*** Associating and Creating links"
    net.addLink(ap1, ap2)
    net.addLink(ap1, ap3)
    net.addLink(ap1, ap4)
    net.addLink(ap2, ap3)
    net.addLink(ap2, ap4)
    net.addLink(ap3, ap4)

    net.addLink(ap1, h1)
    net.addLink(ap1, sta1)
    net.addLink(ap1, sta2)
    net.addLink(ap2, sta3)
    net.addLink(ap3, sta4)
    net.addLink(ap4, sta5)
    net.addLink(ap4, sta6)
    print "*** Starting network"
    net.build()
    c1.start()
    ap1.start( [c1] )
    ap2.start( [c1] )
    ap3.start( [c1] )
    ap4.start( [c1] )
    
    net.seed(10)

    """uncomment to plot graph"""
    net.plotGraph(max_x=100, max_y=100)

    net.startMobility(startTime=0, model='RandomWayPoint', max_x=60, max_y=60, min_v=0.1, max_v=0.5, AC='ssf')

   

    print "*** Running CLI"
    CLI( net )

    print "*** Stopping network"
    net.stop()

if __name__ == '__main__':
    setLogLevel( 'info' )
    topology()
