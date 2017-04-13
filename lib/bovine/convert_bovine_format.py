#------------------------------
# BEGIN func: convert_bovine_format
#------------------------------
def convert_bovine_format(indict, hosts={}, groups={}, level=0, keytype='toplevel'):
  #this function takes a hash in the new inventory format,
  #and returns another hash in the expected ansible dymamic inventory format

  #------------------------------
  # loop through key/value pairs
  #------------------------------
  for k,v in indict.iteritems():

    if (vagrant_mode == '0') and (k == 'vagranthosts'):
      if debug_mode and debug_bovine:
        print "    " * level, "DEBUG: *******************************"
        print "    " * level, "DEBUG: we should skip vagranthosts now"
        print "    " * level, "DEBUG: *******************************"

      return

    if k == 'groups':
      #add the group name to the list of groups
      group = None
      for group in v:
          #add the group with a default vars: {}
          #  this fixes an older bug (no longer an issue?)
          #  where groups with no vars acted strangely
          newgroup = { group: { 'vars': {} } }
          groups = data_merge(groups, newgroup)

          #if debug_mode:
          #  print >> sys.stderr, "DEBUG: top group = ", group

    #*********************
    if debug_mode and debug_bovine:
      print "    " * level, "DEBUG: *******************************"
      print "    " * level, "DEBUG: Key       = ", k
      print "    " * level, "DEBUG: Key Type  = ", keytype
      print "    " * level, "DEBUG: Value     = ", v
      print "    " * level, "DEBUG: vagrant_mode     = ", vagrant_mode
      print "    " * level, "DEBUG: vagrant_mode type     = ", type(vagrant_mode)
      print "    " * level, "DEBUG: *******************************"
    #*********************

    if isinstance(v, dict):
      #---
      # if this key/level has more groups underneath it
      #---
      if 'groups' in v:
        group = None #reinit for reuse
        newgroups = { k: { 'children': [], 'vars': {} } }

        for group in v['groups']:
          #*********************
          #if debug_mode and debug_bovine_groups:
          #  print >> sys.stderr, "DEBUG: group =        ", group
          #  print >> sys.stderr, "DEBUG: parent_group = ", k
          #  print ""
          #*********************

          #add each child group as 'children' to parent group
          newgroups[k]['children'].append(group)

          #*********************
          #if debug_mode and debug_bovine_groups:
          #  print >> sys.stderr, "DEBUG: newgroups = ", newgroups
          #*********************

        #add temp newgroups to groups
        #*********************
        #if debug_mode and debug_bovine_groups:
        #  print "***********************************"
        #  print >> sys.stderr, "DEBUG: groups before = ", groups
        #*********************

        groups = data_merge(groups, newgroups)

        #*********************
        #if debug_mode and debug_bovine_groups:
        #  print >> sys.stderr, "DEBUG: groups after = ", groups
        #  print "***********************************"
        #*********************

      ##---
      ## if this key/level finally contains hosts
      ##---
      if 'hosts' in v:
        #*********************
        if debug_mode and debug_bovine_hosts:
          print >> sys.stderr, "DEBUG: key        = ", k
          print >> sys.stderr, "DEBUG: v          = ", v
          print >> sys.stderr, "DEBUG: v['hosts'] = ", v['hosts']
        #*********************

        newhosts = {}
        newgroups = { k: { 'hosts': [] } }
        host = None

        if isinstance(v['hosts'], list):
          print >> sys.stderr, "Hosts as an array should not contain list:"
          print >> sys.stderr, ""
          print >> sys.stderr, "key = ", k
          print >> sys.stderr, "key's value = ", v
          print >> sys.stderr, ""
          print >> sys.stderr, "Specifically, the 'hosts': contains"
          print >> sys.stderr, v['hosts']
          print >> sys.stderr, ""
          print >> sys.stderr, "  e.g."
          print >> sys.stderr, "  Do this:"
          print >> sys.stderr, "    hosts:"
          print >> sys.stderr, "      host1:"
          print >> sys.stderr, "      host2:"
          print >> sys.stderr, "  Instead of this:"
          print >> sys.stderr, "    hosts:"
          print >> sys.stderr, "      - host1"
          print >> sys.stderr, "      - host2"
          print >> sys.stderr, ""
          print >> sys.stderr, "Exiting: return code 1"
          exit(1)

        for host in list( v['hosts'] ):
        #for host in v['hosts']:
          #if debug_mode:
          #  print >> sys.stderr, "DEBUG: v.host._host = ", v['hosts'][host]

          if (
            v['hosts'][host]
            and
            'vars' in v['hosts'][host]
            and
            'ec2_hosts' in v['hosts'][host]['vars']
            and
            host in v['hosts'][host]['vars']['ec2_hosts']
            and
            'exist' in v['hosts'][host]['vars']['ec2_hosts'][host]
            and
            v['hosts'][host]['vars']['ec2_hosts'][host]['exist'] > 1
          ):
            #do not add scaled cluster names as individual hosts
            #add to custom group for later referencing their parent_group in this function
            newgroups['ec2_hosts_scaled'] = {
              host: {
                'exist': v['hosts'][host]['vars']['ec2_hosts'][host]['exist'],
                'parent_group': k,
              }
            }
          elif (
            v['hosts'][host]
            and
            'vars' in v['hosts'][host]
            and
            'ec2_hosts' in v['hosts'][host]['vars']
            and
            host in v['hosts'][host]['vars']['ec2_hosts']
            and
            'exist' in v['hosts'][host]['vars']['ec2_hosts'][host]
            and
            v['hosts'][host]['vars']['ec2_hosts'][host]['exist'] == 0
          ):
            #do not add hosts set to exist: 0
            pass
          else:
            # add each host to _meta.hostvars
            newhosts[host] = v['hosts'][host]

            ## if this host contains nothing (i.e. no vars),
            ## initialize it to an empty dict
            if v['hosts'][host] is None:
              newhosts[host] = { }
            else:
              if 'vars' in v['hosts'][host]:
                newhosts[host] = v['hosts'][host]['vars']

            # also add each host to the 'hosts' hash under its group
            newgroups[k]['hosts'].append(host)

            #if debug_mode:
            #  print >> sys.stderr, "DEBUG: newhosts = ", newhosts

            #*********************
            if debug_mode and debug_bovine_hosts:
              print >> sys.stderr, "DEBUG: host       = ", host
              print >> sys.stderr, "DEBUG: type v['hosts'] = ", type(v['hosts'])
              print >> sys.stderr, "DEBUG: v['hosts'][host] = ", v['hosts'][host]
              print >> sys.stderr, "DEBUG: type of v['hosts'][host] = ", type(v['hosts'][host])
              print >> sys.stderr, "DEBUG: newhosts[host] = ", newhosts[host]
              print >> sys.stderr, ""
            #*********************


          hosts = data_merge(hosts, newhosts)
          groups = data_merge(groups, newgroups)

      ##---
      ## if this key/level contains 'parent_groups'
      ##---
      if 'parent_groups' in v:
        if debug_mode and debug_bovine_parent_groups:
          print >> sys.stderr, "DEBUG: key = ", k
          print >> sys.stderr, "DEBUG: value = ", v
          print >> sys.stderr, ""

        if v['parent_groups'] is None:
          pass #just don't add the parent_groups
        else:

          #is the current key a group or a host?
          if keytype == 'group':
            newgroups = {}
            group = None
            for group in v['parent_groups']:
              newgroups[group] = { 'children': [ k ] }
            groups = data_merge(groups, newgroups)

          elif keytype == 'host':
            newgroups = {}
            group = None
            for group in v['parent_groups']:
              newgroups[group] = { 'hosts': [ k ] }
            groups = data_merge(groups, newgroups)


      #---
      # if this key/level contains 'vars'
      #---

      #*********************
      if debug_mode and debug_bovine_vars:
          print >> sys.stderr, "DEBUG: k = ", k
      #*********************

      if 'vars' in v:
        #*********************
        if debug_mode and debug_bovine_vars:
          print >> sys.stderr, "DEBUG: v['vars'] = ", v['vars']
        #*********************

        if v['vars'] is None:
          pass #just ignore it

        else:
          newgroups = {}

          #----------
          # special exception for ec2_hosts embedded in other groups
          #----------
          if 'ec2_hosts' in list( v['vars'] ):
            newgroups['all'] = { 'vars': { 'ec2_hosts': {} } }
            newgroups['_meta'] = { 'hostvars': {} }

            for ec2_host in list( v['vars']['ec2_hosts'] ):

              #*********************
              if debug_mode and debug_bovine_vars_ec2:
                print >> sys.stderr, "DEBUG: ec2_host  = ", ec2_host
                print >> sys.stderr, "DEBUG: v['vars'] = ", json.dumps(v['vars'], indent=4)
                if 'exist' in v['vars']['ec2_hosts'][ec2_host]:
                  print >> sys.stderr, "DEBUG: exist  = ", v['vars']['ec2_hosts'][ec2_host]['exist']
                print >> sys.stderr, ""
              #*********************

              if (
                'exist' in v['vars']['ec2_hosts'][ec2_host]
                and
                v['vars']['ec2_hosts'][ec2_host]['exist'] > 1
              ):
                count = v['vars']['ec2_hosts'][ec2_host]['exist']

                temp_parent_group = str( groups['ec2_hosts_scaled'][ec2_host]['parent_group'] )
                newgroups[temp_parent_group] = { 'hosts': [] }

                for num in range(0,count):
                  newgroups['all']['vars']['ec2_hosts'][str(ec2_host) + str(num + 1)] = copy.deepcopy( v['vars']['ec2_hosts'][ec2_host] )
                  newgroups['all']['vars']['ec2_hosts'][str(ec2_host) + str(num + 1)]['exist'] = 1
                  #newgroups['_meta']['hostvars'][str(ec2_host) + str(num + 1)] = { 'ec2_vars': copy.deepcopy( v['vars']['ec2_hosts'][ec2_host] ) }
                  newgroups['_meta']['hostvars'][str(ec2_host) + str(num + 1)] = copy.deepcopy( v['vars'] )
                  newgroups['_meta']['hostvars'][str(ec2_host) + str(num + 1)]['cluster_name'] = str(ec2_host)

                  # also add each host to the 'hosts' list under its group
                  newgroups[temp_parent_group]['hosts'].append(str(ec2_host) + str(num + 1))

                  #*********************
                  if debug_mode and debug_bovine_vars_ec2:
                    print >> sys.stderr, "DEBUG: for ec2_host = ", ec2_host
                    print >> sys.stderr, "DEBUG: num = ", num
                    print >> sys.stderr, "DEBUG: scaled hostname = ", str(ec2_host) + str(num + 1)
                    print >> sys.stderr, "DEBUG: id(vars) = ", id(v['vars']['ec2_hosts'][ec2_host])
                    print >> sys.stderr, "DEBUG: id(newgroup vars) = ", id( newgroups['_meta']['hostvars'][str(ec2_host) + str(num + 1)] )
                    print >> sys.stderr, "DEBUG: (newgroup vars) = ",  newgroups['_meta']['hostvars'][str(ec2_host) + str(num + 1)]
                    print >> sys.stderr, ""
                  #*********************

              else:
                newgroups['all']['vars']['ec2_hosts'].update({ec2_host: { }})
                newgroups['all']['vars']['ec2_hosts'][ec2_host].update(v['vars']['ec2_hosts'][ec2_host])

                #*********************
                if debug_mode and debug_bovine_vars_ec2:
                  print >> sys.stderr, "DEBUG: ec2_hosts = ", json.dumps(newgroups['all']['vars']['ec2_hosts'], indent=4)
                  print >> sys.stderr, ""
                #*********************

          else: #not ec2_hosts
            newgroups[k] = { 'vars': v['vars'] }
          #----------

          #*********************
          if debug_mode and debug_bovine_vars:
            print >> sys.stderr, "DEBUG: newgroups = ", newgroups
            print >> sys.stderr, ""
          #*********************
          groups = data_merge(groups, newgroups)


      #---
      # continue descending recursively
      #---
      level = level + 1 #level var just for debugging (<- still the case?)
      if debug_mode and debug_bovine:
        print "    " * level, "DEBUG: Descending....", "level = ", level

      if k == 'groups':
        newkeytype = 'group'
      elif k == 'hosts':
        newkeytype = 'host'
      else:
        if keytype == 'host':
          newkeytype = 'hostdata'
        elif keytype == 'group':
          newkeytype = 'groupdata'
        else:
          newkeytype = 'data' #we should NEVER get here

      convert_bovine_format(v, hosts, groups, level=level, keytype=newkeytype)

      level = level - 1
      if debug_mode and debug_bovine:
        print "    " * level, "DEBUG: Ascending.... level = ", level

  #------------------------------
  # END loop through key/value pairs
  #------------------------------

  if level == 0:
    outdict = {
      '_meta': {
        'hostvars': hosts
      }
    }


    #*********************
    if debug_mode and debug_bovine_outdict:
      print "***********************************"
      print >> sys.stderr, "DEBUG: outdict before = "
      print json.dumps(
        outdict, indent=4
      )
      print "***********************************"
    #*********************

    outdict = data_merge(outdict, groups)

    #*********************
    if debug_mode and debug_bovine_outdict:
      print "***********************************"
      print >> sys.stderr, "DEBUG: outdict after = "
      print json.dumps(
        outdict, indent=4
      )
      print "***********************************"
    #*********************

    return outdict

#------------------------------
# END func: convert_bovine_format
#------------------------------
