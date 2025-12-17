// find the groups of overlapping lookups
List<Annotation> lookups = new ArrayList<Annotation>(inputAS.get("Lookup"));

// there are no lookups so nothing to do
if (lookups.size() == 0) return;

List<Set<Annotation>> groups = new ArrayList<Set<Annotation>>()
while (lookups.size() > 0) {
    Annotation a = lookups.remove(0);
    
    Set<Annotation> group = new HashSet<Annotation>();
    group.add(a);
    
    // I think this might miss cases where two annotations don't overlap
    // each other but are overlapped by a third. Depending on what order
    // you hit these you might not get all of them. Need to design some
    // tests for that and maybe need a recursive function to get them all
    group.addAll(gate.Utils.getContainedAnnotations(inputAS.get("Lookup"), a));
    group.addAll(gate.Utils.getCoveringAnnotations(inputAS.get("Lookup"), a));
    group.addAll(gate.Utils.getOverlappingAnnotations(inputAS.get("Lookup"), a));
    
    lookups.removeAll(group)
    
    groups.add(new ArrayList<Annotation>(group))
}

if (groups.size() == 1) {

    a = getLongestBySpan(groups.get(0)).get(0);
    FeatureMap feats = Factory.newFeatureMap();
    feats.putAll(a.getFeatures())
    gate.Utils.addAnn(outputAS, a, "Location", feats)
    
    return;
}

// pick an initial set of points (pick one from each set either randomly or closest to centroid)

List<Annotation> points = new ArrayList<Annotation>();
for (group in groups)
    points.add(group.get(0))


// this is the size of the bounding box given the initial points
float size = getSize(points)

while (true) {

    boolean changed = false
    
    for (int i = 0 ; i < groups.size() ; ++i) {
        group = groups.get(i)
        Annotation current = points.get(i);
        
        for (int j = 0 ; j < group.size() ; ++j) {
            next = group.get(j);
            
            if (current.equals(next)) continue;
            
            points.set(i,next);
            
            float s = getSize(points);
            
            if (s < size) {
                size = s
                changed = true
                current = next
            } else {
                points.set(i,current)
            }
        }
    }

    if (!changed) break;
}

for (Annotation a : points) {
    FeatureMap feats = Factory.newFeatureMap();
    feats.putAll(a.getFeatures())
    gate.Utils.addAnn(outputAS, a, "Location", feats)
}

def getLongestBySpan(Collection<Annotation> annots) {
    List<Annotation> selected = new ArrayList<Annotation>();
    
    long length = 0
    
    for (Annotation a : annots) {
        long len = a.getEndNode().getOffset() - a.getStartNode().getOffset();
    
        if (selected.isEmpty()) {
            selected.add(a)
            length = len
        }
        else {
            
            if (len == length) {
                selected.add(a)
            }
            else if (len > length) {
                selected.clear();
                selected.add(a)
                length = len
            }
        }
    }
    
    return selected
}

def getSize(Collection<Annotation> points) {
    
    Float min_lon = null
    Float max_lon = null
    Float min_lat = null
    Float max_lat = null
    
    for (Annotation p in points) {
    
        float lon = Float.valueOf(p.getFeatures().get("lon"))
        float lat = Float.valueOf(p.getFeatures().get("lat"))
    
        if (lon < 0) lon += 360
    
        if (min_lon == null) {
            min_lon = lon
            max_lon = lon
            min_lat = lat
            max_lat = lat
        } else {
            min_lon = Math.min(min_lon,lon);
            max_lon = Math.max(max_lon,lon);
            min_lat = Math.min(min_lat,lat);
            max_lat = Math.max(max_lat,lat);
        }
    }
    
    float size = (max_lon-min_lon)*(max_lat-min_lat)
    
    return size
}